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
from requests import get
from bs4 import BeautifulSoup
from .extractors.wwr import extract_wwr_jobs
from .extractors.programmers import extract_programmers_jobs
import numpy
import pandas as pd

def crawl():
    #programmers > programmers.csv
    page_num = 1
    programmers = extract_programmers_jobs(page_num) # list

    #list -> DataFrame
    df = pd.DataFrame.from_dict(programmers)
    #DataFrame -> json
    df_string = df.to_json(orient = 'index')
            
    res = httpx.post("http://localhost:8000/crawl_data", data=df_string)
    print(res)
    res = httpx.post("http://localhost:8002/send_data", data=df_string)
    print(res)
    
    return df_string


@router.get("/programmers_crawl", tags=["slack"])
async def programmers_crawl():
    try:
        dat = crawl()
        return dat
    except Exception as e:
        print(e)
        return "NO"