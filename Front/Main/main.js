document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("cover-letter-form").addEventListener("submit", async function(event) {
        event.preventDefault();  // 폼의 기본 동작을 막음

        const job = document.getElementById("job").value;
        const question = document.getElementById("question").value;
        const answer = document.getElementById("answer").value;

        try {
            // 데이터를 백그라운드에서 전송
            const response = await fetch('http://localhost:8000/api/submit', {  // FastAPI 서버의 엔드포인트
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    job: job,
                    question: question,
                    answer: answer
                })
            });

            if (!response.ok) {
                throw new Error('서버 응답 오류');
            }

            const data = await response.json();
            console.log('성공:', data);

            // 서버에서 받은 피드백 데이터를 localStorage에 저장
            localStorage.setItem('job', job);
            localStorage.setItem('question', question);
            localStorage.setItem('answer', answer);
            localStorage.setItem('feedback', data.feedback);

            // 결과 페이지로 리다이렉트
            window.location.href = '../Result/result.html';

        } catch (error) {
            console.error('전송 오류:', error);
            // 로딩 아이콘을 숨기고 오류 페이지로 이동
            document.getElementById("loading-overlay").style.display = "none";
            window.location.href = 'error.html';  // 오류 발생 시 오류 페이지로 이동
        }
    });
});
