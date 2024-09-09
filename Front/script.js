document.getElementById("cover-letter-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    const job = document.getElementById("job").value;
    const question = document.getElementById("question").value;
    const answer = document.getElementById("answer").value;

    console.log("지원 직무:", job);
    console.log("자기소개서 문항:", question);
    console.log("자기소개서 답변:", answer);

    // 버튼 애니메이션 추가
    const button = document.querySelector("button");
    button.classList.add("submitted");
    setTimeout(() => {
        button.classList.remove("submitted");
    }, 600);

    // 추가적으로 폼 제출 작업 수행
});
