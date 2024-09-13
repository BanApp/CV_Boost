document.addEventListener("DOMContentLoaded", function() {
    // 로컬 스토리지에서 데이터 가져오기 및 표시
    document.getElementById('job').innerText = localStorage.getItem('job');
    document.getElementById('question').innerText = localStorage.getItem('question');
    document.getElementById('answer').innerText = localStorage.getItem('answer');
    document.getElementById('feedback').innerText = localStorage.getItem('feedback');

    // 초기화면으로 돌아가기 버튼 클릭 이벤트
    document.getElementById('go-back').addEventListener('click', function() {
        window.location.href = '../Main/main.html'; // 초기화면으로 이동
    });

    // 저장하기 버튼 클릭 이벤트
    document.getElementById('save-feedback').addEventListener('click', function() {
        const job = document.getElementById('job').innerText;
        const question = document.getElementById('question').innerText;
        const answer = document.getElementById('answer').innerText;
        const feedback = document.getElementById('feedback').innerText;

        const feedbackData = {
            job: job,
            question: question,
            answer: answer,
            feedback: feedback
        };

        // 피드백 데이터를 JSON 형식으로 저장 (이 예시에서는 파일 저장 기능을 대신하여 콘솔에 표시)
        console.log('저장된 피드백:', JSON.stringify(feedbackData));

        alert('피드백이 성공적으로 저장되었습니다!');
    });

    // 피드백 복사 버튼 클릭 이벤트
    document.getElementById('copy-feedback').addEventListener('click', function() {
        const feedbackText = document.getElementById('feedback').innerText;
        navigator.clipboard.writeText(feedbackText).then(function() {
            alert('피드백이 클립보드에 복사되었습니다.');
        }, function(err) {
            alert('복사 실패: ' + err);
        });
    });
});
