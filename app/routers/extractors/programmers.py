from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from time import time, sleep
from tqdm import tqdm


"""
프로그래머스 웹페이지 크롤링 프로세스
1. 크롤링할 페이지 수를 설정한다.
2. 1에서 설정한 개수만큼 페이지를 이동하면서 채용 공고문의 링크를 크롤링한다.
3. 2에서 크롤링한 공고문의 링크를 각각 들어가서 원하는 데이터를 크롤하여, 딕셔너리 형태로 저장한다.
4. 채용 공고문 딕셔너리를 담고 있는 리스트를 반환한다.
"""

def extract_programmers_jobs(page_num):
    #1. 크롤링할 페이지 수를 설정한다.
    page_num = page_num

    #2. 1에서 설정한 개수만큼 페이지를 이동하면서 채용 공고문의 링크를 크롤링한다.
    options = Options()
    options.add_argument('headless')
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager().install()) #크롬 브라우저 버전이 업데이트 되면 그에 맞는 크롬 드라이버 설치
    driver = webdriver.Chrome(service=service, options=options)
    
    sleep(3)
    
    url = "https://career.programmers.co.kr/job"
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    post_urls = ["https://career.programmers.co.kr" + position_link['href'] for position_link in soup.find_all("a", class_="position-link")] # 채용 공고문의 링크를 저장하는 리스트

    for _ in range(page_num - 1):
        #다음 페이지로 이동 
        next_page_btn = 'ul.pagination > li:last-child'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_page_btn))).click()
        
        sleep(10)

        html = driver.page_source # get page source(html) from driver
        soup = BeautifulSoup(html, "html.parser") # parse page source(html)
        post_urls = post_urls + ["https://career.programmers.co.kr" + position_link['href'] for position_link in soup.find_all("a", class_="position-link")] 


    #3. 2에서 크롤링한 공고문의 링크를 각각 들어가서 원하는 데이터를 크롤링한 후, 딕셔너리 형태로 저장한다.
    results = []
    for post_url in tqdm(post_urls):
        driver.get(post_url)
        driver.implicitly_wait(3)

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #결측값 대비
        site_name = "" 
        url = "" 
        title = "" 
        collection_date = "" 
        start_date = "" 
        end_date = "" 
        company_name = "" 
        location = "" 
        recruit_field = "" 
        recruit_type = "" 
        recruit_classification = "" 
        personnel = "" 
        salary = "" 
        position = "" 
        task = "" 
        qualification = "" 
        prefer = "" 
        welfare = "" 
        description = "" 
        stacks = ""

        #site_name
        site_name = "programmers"

        #post_url(공고 url)
        url = post_url

        #title(공고 제목)
        try:
            title = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/h2').text
            #title = title.replace(",","/")
        except:
            pass

        #collection_date
        collection_date = time()
        collection_date = int(collection_date)
        collection_date = str(collection_date)

        #start_date(공고 시작일) is not provided from the site.

        #end_date(공고 마감일)
        try:
            end_date = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[2]/div[2]').text
        except:
            pass

        #company_name(회사 이름)
        try:
            company_name = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').text
        except:
            pass

        #location(회사 위치)
        try:
            location = driver.find_element(By.CSS_SELECTOR, 'div.oSd94NeynGy8qiuPFFgg > div:nth-child(2) > div > div:last-child').text
            #location = location.replace(",", "/")
        except:
            pass

        #recruit_field(채용 분야) is not provided from the site.
        

        #recruit_type(고용 형태) #정규직
        try:
            recruit_type = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[3]/div[2]').text 
        except:
            pass       

        #recruit_classification(채용 구분) is not provided from the site.

        #personnel(채용 인원) is not provided from the site.

        #salary(급여)
        try:
            salary = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[5]/div[2]').text
        except:
            pass

        #position(회사에서 원하는 포지션) #직무
        try:
            position = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[1]/div[2]').text
            #position = position.replace(",", "/")
        except:
            pass

        #task(하는 업무) is not provided from the site.

        #qualification(자격 요견) is not provided from the site.

        #prefer(우대 사항) is not provided from the site.

        #welfare(복지) is not provided from the site.

        #description(설명) is not provided from the site.

        #stacks(기술 스택)
        try:
            #리스트 형태 데이터
            stacks = [tech_stack.text for tech_stack in driver.find_elements(By.CSS_SELECTOR, 'li.QdgvMJO9ZYOaiwrEUqgo.nUBs27jXBxRVUu9DLzz4')]
            stacks = "/".join(stacks) #convert list to string
        except:
            pass
        
        """
        #경력
        try:
            experience = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/section/div/div[1]/div[4]/div[2]').text
        except:
            pass
        """

        """
        #평균 응답 시간
        try:
            response_speed = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/div/span').text
        except:
            pass
        """

        """
        #회사 소개 링크
        try:
            company_link = driver.find_element(By.XPATH, '//*[@id="career-app-legacy"]/div/div[1]/div[1]/header/div/div[2]/h4/a').get_attribute('href')
        except:
            pass
        """

        job_data = {
                'sitename': site_name,
                'title': title,
                'url': url,
                'collectiondate': collection_date,
                'startdate': start_date,
                'enddate': end_date,
                'companyname': company_name,
                'location': location,
                'recruitfield': recruit_field,
                'recruittype': recruit_type,
                'recruitclassification': recruit_classification,
                'personnel': personnel,
                'salary': salary,
                'position': position,
                'task': task,
                'qualification': qualification,
                'prefer': prefer,
                'welfare': welfare,
                'description': description,
                'stacks': stacks
            }
        results.append(job_data)
    driver.close()
    #4. 채용 공고문 딕셔너리를 담고 있는 리스트를 반환한다.
    return results
