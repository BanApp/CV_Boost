document.addEventListener("DOMContentLoaded", function() {
    const timeout = 300000; // 5분을 밀리초로 변환
    let pollingInterval = 5000; // 5초마다 상태를 확인하도록 설정

    // 상태 확인 함수
    const checkStatus = async () => {
        try {
            // 상태 확인을 위한 엔드포인트는 필요 없으므로 이 부분은 삭제되었습니다.
            // 서버에서 결과를 직접 확인하는 대신 결과 페이지로 이동합니다.
            
            // 예제: 서버에서 결과를 확인하는 엔드포인트가 필요할 경우, 다음과 같은 요청을 사용합니다.
            // const response = await fetch('http://localhost:8000/api/status');
            // if (!response.ok) {
            //     throw new Error('네트워크 응답이 좋지 않습니다');
            // }
            // const data = await response.json();

            // 결과 페이지로 이동
            window.location.href = 'result.html';
        } catch (error) {
            console.error('오류:', error);
            window.location.href = 'index.html'; // 오류 발생 시 메인 페이지로 이동
        }
    };

    // 주기적으로 상태를 확인
    const poll = setInterval(() => {
        checkStatus();
    }, pollingInterval);

    // 타임아웃 설정
    setTimeout(() => {
        clearInterval(poll); // 타임아웃 후 폴링 중지
        window.location.href = 'index.html'; // 시간 초과 시 메인 페이지로 이동
    }, timeout);
});
