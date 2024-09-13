from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time
import re

# FastAPI 애플리케이션 생성
app = FastAPI()

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서 요청을 허용합니다. 보안상 필요한 출처만 허용하는 것이 좋습니다.
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용합니다.
    allow_headers=["*"],  # 모든 헤더를 허용합니다.
)

# 모델 로딩
FINETUNE_MODEL = './Model'

finetune_model = AutoModelForCausalLM.from_pretrained(FINETUNE_MODEL, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained('./saved_tokenizer')

# Tokenizer 저장

pipe_finetuned = pipeline("text-generation", model=finetune_model, tokenizer=tokenizer, max_new_tokens=512)

def process_response(response_text):
    # "개선점:" 단어를 제거
    response_text = response_text.replace("개선점:", "").strip()
    
    # 문단 구분을 위한 패턴 설정 (예: 여러 개의 공백, 줄바꿈 등)
    paragraphs = re.split(r'\n\s*\n', response_text)
    
    # 각 문단을 한 줄씩 띄어 구분하여 결과 생성
    processed_text = '\n\n'.join(paragraphs)
    
    return processed_text

# 데이터 모델 정의
class Submission(BaseModel):
    job: str
    question: str
    answer: str

# API 엔드포인트 정의
@app.post("/api/submit")
async def submit_form(submission: Submission):
    try:
        # 수신된 데이터 출력
        print(f"Job: {submission.job}")
        print(f"Question: {submission.question}")
        print(f"Answer: {submission.answer}")
        start_time = time.time()

        # 사용자로부터 받은 입력을 바탕으로 텍스트 생성
        messages = [
            {
                "role": "user",
                "content": (
                    f"자기소개서 문항에 대해서 지원자가 작성한 자기소개서 답변을 지원 직무를 고려하여, 채용 담당자 관점에서 개선점을 피드백 해주세요.\n"
                    f"지원 직무: {submission.job}\n"
                    f"자기소개서 문항: {submission.question}\n"
                    f"자기소개서 답변: {submission.answer}"
                )
            }
        ]

        prompt = pipe_finetuned.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        outputs = pipe_finetuned(
            prompt,
            do_sample=True,
            temperature=0.6,
            top_k=50,
            top_p=0.95,
            add_special_tokens=True
        )
        
        response_text = outputs[0]["generated_text"][len(prompt):]
        processed_text = process_response(response_text)

        print(processed_text)
        # 종료 시간 기록
        end_time = time.time()

        # 경과 시간 계산
        elapsed_time = end_time - start_time
        print(f"경과 시간: {elapsed_time:.2f}초")

        # 성공적인 응답 반환
        return {"message": "Form submission successful", "status": "success", "feedback": processed_text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))