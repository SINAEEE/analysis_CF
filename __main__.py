import urllib
from itertools import count
from bs4 import BeautifulSoup
import pandas as pd
import xml.etree.ElementTree as et
import time
from selenium import webdriver
import collection.crawler as cw
from collection.data_dict import sido_dict, gungu_dict

RESULT_DIRECTORY = '__result__/crawling'

def crawling_pericana():
    results = []
    #for page in range(1,3):
    for page in count(start=1):
         url = 'http://www.pelicana.co.kr/store/stroe_search.html?gu=&si=&page=%d' % page
         html = cw.crawling(url=url)

         bs = BeautifulSoup(html, 'html.parser')
         tag_table = bs.find('table', attrs={'class': 'table mt20'})
         tag_tbody = tag_table.find('tbody')
         tags_tr = tag_tbody.findAll('tr')

         #끝 검출
         if len(tags_tr) == 0:
             break;

         #print(page, ":", len(tags_tr), sep=":")

         for tag_tr in tags_tr:
             strings = list(tag_tr.strings)
             name = strings[1]
             address = strings[3]
             #print(address.split())
             sidogu = address.split()[:2]

             results.append( (name, address) + tuple(sidogu)) #튜플만들기

    #store
    table = pd.DataFrame(results, columns=['name','address','sido','gungu'])
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v,v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/pericana_table.csv'.format(RESULT_DIRECTORY),
         encoding='utf-8',
         mode='w',
         index=True)


    #print(results)

def proc_nene(xml):
    root = et.fromstring(xml)
    results = []

    elements_item = root.findall('item')
    for el in elements_item:
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name, address, sido, gungu))

    return results


def store_nene(data):
    table = pd.DataFrame(data, columns=['name','address','sido','gungu'])
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v,v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/nene_table.csv'.format(RESULT_DIRECTORY),
         encoding='utf-8',
         mode='w',
         index=True)

"""
def crawling_kyochon():
    for sido1 in range(1,18):
        for sido2 in count(start=1):
            if condition:
                break
"""

def crawling_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    #첫 페이지 로딩
    wd = webdriver.Chrome('D:/bigdatastudy/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(5)
    #print(wd.page_source)

    for page in range(101,105):
        #자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        time.sleep(5)

        #실행결과 HTML(redering 된 HTML) 가져오기
        html = wd.page_source

        #parsing with bs4
        bs = BeautifulSoup(html,'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id':'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        #마지막 검출
        if tags_tr[0].get('class') is None:
            break

        print(tag_tbody)




if __name__ == '__main__':

    #pelicanas
    #crawling_pericana()

    #nene
    """
    cw.crawling(
        url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s'
            % (urllib.parse.quote("전체"), urllib.parse.quote("전체")),
        proc = proc_nene,
        store = store_nene)
    """

    #kyochon
    #crawling_kyochon()

    #goobne
    crawling_goobne()




    """
    #def my_error(e):
    #    print("my error : " + str(e))
    
    def proc(html):
        print("processing..... " + html)
    
    def store(result):
        pass
    
    
    
    result = cw.crawling(
        url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
        encoding='cp949',
        proc=proc,
        store=store)
        #err=my_error)
    
    print(result)
    #print("processing..."+result)
    """
