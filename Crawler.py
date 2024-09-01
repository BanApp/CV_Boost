from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import openpyxl
from openpyxl import Workbook
import re
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    ElementNotInteractableException,
    UnexpectedAlertPresentException,
    NoSuchElementException,
    NoAlertPresentException
)
# 로그인

# 잡코리아 id, 비밀번호
user_id = ""
user_pw = ""
def login_protocol(driver: webdriver.Chrome):
    driver.get("https://www.jobkorea.co.kr/")

    try:
        # Wait for the login button to be clickable and click it
        wait = WebDriverWait(driver, 5)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'로그인')]")))
        login_button.click()

        # Wait for the username and password fields to be present
        id_element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='id']")))
        id_element.send_keys(user_id)
        password_element = driver.find_element(By.XPATH, "//input[@name='password']")
        password_element.send_keys(user_pw)

        input("CAPTCHA를 입력한 후 엔터를 누르세요: ")

        # Click the login button
        login_submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_submit_button.click()

        print("로그인 성공")

        # Wait for navigation to the success page
        print("합격자소서 페이지로 이동 중...")
        success_page_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'합격자소서')]")))
        success_page_link.click()

        input("팝업 창을 닫은 후 엔터를 누르세요: ")
        driver.implicitly_wait(5)

    except Exception as e:
        print(f"문제가 발생했습니다: {e}")


def remove_control_characters(s):
    # 제어 문자를 제거하는 정규식 패턴
    control_char_regex = re.compile(r'[\r\n\t\x00-\x1f\x7f-\x9f]')
    # 특정 문자열 리스트
    unwanted_strings = ["아쉬운점 1", "아쉬운점 2", "아쉬운점 3", "아쉬운점 4", "아쉬운점 5", "아쉬운점 6",
                        "좋은점 1", "좋은점 2", "좋은점 3", "좋은점 4", "좋은점 5", "좋은점 6"]
    #unwanted_strings = []

    # 제어 문자 제거
    cleaned_string = re.sub(control_char_regex, '', s)

    # 특정 문자열 제거
    for string in unwanted_strings:
        cleaned_string = cleaned_string.replace(string, " ")

    return cleaned_string


def extract_good_and_bad_points(text):
    """
    주어진 텍스트에서 '좋은점 {n} 내용' 및 '아쉬운점 {n} 내용' 구조의 문장 중 내용만을 추출하여 각각 리스트로 반환합니다.

    :param text: 분석할 텍스트
    :return: (좋은점 내용 리스트, 아쉬운점 내용 리스트)
    """
    # 정규 표현식을 사용하여 '좋은점 {n} 내용' 구조의 문장 및 '아쉬운점 {n} 내용' 구조의 문장을 찾기
    good_pattern = r'좋은점 \d+ (.*?)(?=아쉬운점 \d+|========|$)'
    bad_pattern = r'아쉬운점 \d+ (.*?)(?=좋은점 \d+|========|$)'

    # '좋은점'과 '아쉬운점'의 모든 매치를 찾음
    good_matches = re.findall(good_pattern, text, re.DOTALL)
    bad_matches = re.findall(bad_pattern, text, re.DOTALL)


    # 각 리스트에서 내용 부분만 가져오기
    good_p = [re.sub(r'좋은점 \d+', '', match).strip() for match in good_matches]
    bad_p = [re.sub(r'아쉬운점 \d+', '', match).strip() for match in bad_matches]

    good_points = ' '.join([match.strip() for match in good_p])
    bad_points = ' '.join([match.strip() for match in bad_p])
    return good_points, bad_points


def scroll_into_view(driver, element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def self_introduction_crawl(driver: webdriver.Chrome):
    excel_path = "your_excel_path.xlsx"  # Excel 파일 경로
    idx = 1
    # 새 워크북 생성 또는 기존 워크북 로드
    try:
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active
    except FileNotFoundError:
        workbook = Workbook()
        sheet = workbook.active
        # 열 제목 추가
        sheet.append(["연도", "시기", "경력", "직무", "회사명", "합격자 정보", "질문", "답변", "장점", "단점", "총평"])

    for i in range(1,178):
        driver.get(f"https://www.jobkorea.co.kr/starter/PassAssay?FavorCo_Stat=0&Pass_An_Stat=1&OrderBy=0&EduType=0&WorkType=0&isSaved=0&Page={i}")
        print(f"현재 페이지 : {i}번")

        try:
            # 'ul' 태그의 클래스 'selfLists' 안의 모든 'a' 태그 찾기
            links = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.logo"))
            )

            # 모든 'href' 속성 값을 리스트에 저장
            hrefs = [link.get_attribute('href') for link in links]

            for href in hrefs:
                try:
                    driver.get(href)

                    # 예시 : 2024년 상반기 신입 앱개발자
                    title_info = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/h2/em"))
                    ).text.split()

                    # 회사 명
                    company_text = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[1]/div[1]/h2/strong/a"))
                    ).text
                    print(f"현재 저장중인 회사 : {company_text}")


                    # specLists 클래스를 가진 ul 태그 안의 모든 li 데이터 가져오기
                    spec_items = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.specLists li"))
                    )
                    spec_list = [item.text for item in spec_items]
                    if spec_list:
                        spec_list.pop()  # 마지막 필요없는 데이터 제거


                    # dt_tx, dd_tx (질문, 답변)
                    dt_tx_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "dl.qnaLists dt button span.tx"))
                    )

                    cnt = 0
                    for dt in dt_tx_elements:
                        # dt 요소를 클릭하여 숨김 해제
                        if cnt > 1:
                            driver.execute_script("arguments[0].click();", dt)
                        cnt += 1

                    dd_tx_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "dl.qnaLists dd div.tx"))
                    )

                    dd_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "dl.qnaLists dd"))
                    )
                    p_tx_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "p.tx"))
                    )

                    p_tx_elements = p_tx_elements * len(dt_tx_elements)

                    advice_elements = WebDriverWait(driver, 5).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.advice"))
                    )

                    for dt_tx, dd_tx, dd, pp, ae in zip(dt_tx_elements, dd_tx_elements, dd_elements, p_tx_elements, advice_elements):
                        try:
                            scroll_into_view(driver, dt_tx)  # 요소를 화면에 보이게 함
                            if dd.get_attribute('class') == "":
                                # Click element using ActionChains
                                actions = ActionChains(driver)
                                actions.move_to_element(dt_tx).click().perform()

                            # p 태그 내용 제거하기
                            p_text = dd_tx.find_element(By.CSS_SELECTOR, "p.txSpllChk").text
                            dd_tx_text = remove_control_characters(dd_tx.text.replace(p_text, ""))
                            gp,bp = extract_good_and_bad_points(ae.text)

                            r_text = pp.text
                            # 데이터 저장
                            sheet.append([title_info[0], title_info[1], title_info[2], title_info[3], company_text,
                                          ', '.join(spec_list), dt_tx.text, dd_tx_text.strip(),gp,bp,r_text])
                            print(f"{idx}번 자기소개서 데이터 저장 완료")
                            idx += 1

                        except ElementNotInteractableException as e:
                            print(f"ElementNotInteractableException 발생: {e}")
                            continue
                        except Exception as e:
                            print(f"질문/답변 처리 중 오류 발생: {e}")
                            continue

                except (UnexpectedAlertPresentException, NoSuchElementException) as e:
                    try:
                        alert = driver.switch_to.alert
                        print(f"Alert detected: {alert.text}")
                        alert.accept()
                    except NoAlertPresentException:
                        print("No alert present after UnexpectedAlertPresentException or NoSuchElementException")
                    finally:
                        continue

        except Exception as e:
            print(f"페이지 처리 중 오류 발생: {e}")
            continue

        print(f"{i}번째 페이지 데이터 : 엑셀 파일 저장 완료")
        # 엑셀 파일 저장하기
        workbook.save(excel_path)

# ChromeDriver 경로를 포함하여 Service 객체를 생성
service = Service(ChromeDriverManager().install())  # MacOS에서의 ChromeDriver 경로
# Service 객체를 사용하여 Chrome 드라이버를 초기화
driver = webdriver.Chrome(service=service)
# 로그인
login_protocol(driver=driver)
# 자기소개서 데이터 크롤링
self_introduction_crawl(driver=driver)
# 드라이버 종료
driver.quit()
