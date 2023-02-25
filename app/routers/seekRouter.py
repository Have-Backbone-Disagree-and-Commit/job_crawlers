from fastapi import APIRouter
router = APIRouter()
import httpx
from datetime import datetime, timedelta
import math
import time
import re
import traceback
from urllib.request import urlopen
import logging
logging.basicConfig(level=logging.INFO)
import numpy
import pandas
from bs4 import BeautifulSoup
import requests

data_columns = [
    'sitename', #사이트명
    'url', #공고 url
    'title', #제목
    'collectiondate', #긁어온 날짜
    'startdate', #공고시작일
    'enddate', #공고마감일
    'companyname', #회사이름
    'location', #회사위치, 근무지
    'recruitfield', #채용분야
    'recruittype', #고용형태
    'recruitclassification', #채용구분
    'personnel', #채용인원
    'salary', #급여
    'position', #회사에서 원하는 포지션
    'task', #하는 업무
    'qualifications',#자격 요건
    'prefer', #우대사항
    'welfare', #복지
    'description', #설명
    'stacks' #기술스택
    ]

def crawl():
    emp_info_all = []
    try:
        sitename = 'SEEK'
        title = ''
        recruitfield = ''
        recruittype = ''
        recruitclassification = ''
        personnel = ''
        salary = ''
        task = ''
        qualifications = ''
        prefer = ''
        welfare = ''
        stacks = ''

        for pageNum in range(1):

            # seek 채용 사이트
            html = urlopen("https://www.seek.com.au/jobs?page=" + str(pageNum) )
            bsObject = BeautifulSoup(html, "html.parser")
                
            # 채용사이트에 개별 링크 가져오기
            emp_url_data = bsObject.find_all('a', class_="_1tmgvw5 _1tmgvw7 _1tmgvwa _1tmgvwb _1tmgvwe yvsb870 yvsb87f _14uh994h")

            # 채용 사이트 개별 링크
            emp_url = []

            # 채용 사이트 링크 emp_link에 넣기
            for data in emp_url_data:
                emp_url.append(data.attrs['href'])

            # 채용 사이트에 하나씩 방문해서 해당 채용 공고 정보 받아오기
            for el in emp_url:

                el_front = 'https://www.seek.com.au'
                html = urlopen(el_front+el)

                # 개별 사이트 링크
                url = el_front+el

                bsObject = BeautifulSoup(html, "html.parser")

                # 제목
                title = bsObject.find('h1', class_="yvsb870 _14uh9944u _1cshjhy0 _1cshjhyl _1d0g9qk4 _1cshjhyp _1cshjhy21").text

                # 회사명
                companyname = bsObject.find('span', class_="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy2 _1cshjhy21 _1d0g9qk4 _1cshjhyd").text

                # 채용 공고 가져오기
                data_all = bsObject.find_all('span', class_="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy21 _1d0g9qk4 _1cshjhya")

                # 가져온 채용 공고를 text 형식으로 emp_info에 넣기
                emp_info = []
                for data in data_all:
                    emp_info.append(data.text)
                    
                # 공고일
                post_all = bsObject.find_all('span', class_="yvsb870 _14uh9944u _1cshjhy0 _1cshjhy1 _1cshjhy22 _1d0g9qk4 _1cshjhya")
                post_ = 0
                # 마지막 값인 날짜만 받아오면 됨
                for pa in post_all:
                    post_ = pa.text

                # 지금 시간
                today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                # today to timestamp
                collectiondate = time.mktime(datetime.strptime(today, '%Y-%m-%d %H:%M:%S').timetuple())
                collectiondate = math.trunc(collectiondate)
                startdate = 0
                enddate = ''
                # h ago, m_ago이면 당일로 계산, d ago이면 오늘날짜 - day
                if 'h ago' in post_ or 'm ago' in post_:
                    startdate = today
                elif 'd ago'in post_:
                    days_ = int(re.sub(r'[^0-9]', '', post_)) #숫자만 추출
                    startdate = (datetime.now() - timedelta(days=days_)).strftime('%Y-%m-%d %H:%M:%S')
                # startdate to timestamp
                startdate = time.mktime(datetime.strptime(startdate, '%Y-%m-%d %H:%M:%S').timetuple())
                startdate = math.trunc(startdate)
                



                # 링크마다 형식이 달라서 start, end 인덱스로 잡음
                start_index = 0
                for ei in emp_info:
                    if(ei >= '0' and ei <= '9') and 'review' in ei:
                        start_index = emp_info.index(ei)+1
                        break
                    else:
                        start_index = emp_info.index('All SEEK products')+1
                    

                # 위치
                location = str(emp_info[start_index])
                # 직무
                position = str(emp_info[start_index+1])
                
                # 설명
                description = ''
                desc_all = bsObject.find_all('li', class_="yvsb870 _14uh9946m")
                for da in desc_all:
                    description += da.text
                    description += '\n'


                #데이터에 값 넣기
                emp_info_all.append([sitename, url, title, collectiondate, startdate, enddate,
                                    companyname, location, recruitfield, recruittype,
                                    recruitclassification, personnel, salary, 
                                    position, task, qualifications, prefer, welfare,
                                    description, stacks])

            
        numpy_emp_info_all = []
        # 배열 -> numpy  
        for eia in emp_info_all:
            numpy_emp_info_all.append(numpy.array(eia))
            # Msg_bot(eia[0], eia[1], eia[2], eia[3], eia[5], eia[6], eia[4])
            # logging.info("success")
            

        # DataFrame -> json
        df_emp_info_all = pandas.DataFrame(numpy_emp_info_all, columns=data_columns)
        # df_string = df_emp_info_all.to_csv("./crawler/seek-crawler/seek_data.csv", index=False, header=False)

        df_string = df_emp_info_all.to_json(orient = 'index')
        
        res = httpx.post("http://localhost:8000/crawl_data", data=df_string)
        print(res)
        res = httpx.post("http://localhost:8002/send_data", data=df_string)
        print(res)

        
    except Exception as e:
        trace_back = traceback.format_exc()
        message = str(e)+ "\n" + str(trace_back)
        logging.error(message)


@router.get("/seek_crawl", tags=["slack"])
async def seek_crawl():
    try:
        crawl()
        return "OK"
    except Exception as e:
        print(e)
        return "NO"