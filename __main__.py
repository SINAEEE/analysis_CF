import urllib
from itertools import count
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
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
         #print(html)

         bs = BeautifulSoup(html, 'html.parser')
         tag_table = bs.find('table', attrs={'class': 'table mt20'})
         tag_tbody = tag_table.find('tbody')
         tags_tr = tag_tbody.findAll('tr')
         #print(type(tags_tr),tags_tr) #type : <class 'bs4.element.ResultSet'>
         #print(len(tags_tr),tags_tr)


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

             results.append((name,address) + tuple(sidogu)) #튜플만들기

             #print(results)

    #store
    table = pd.DataFrame(results, columns=['name','address','sido','gungu'])
    #print(table)
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v,v)) #서울:서울특별시
    #->sido의 기존값을 sido_dict value와 비교하여 있으면 그대로, 없으면 넣는다
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v,v))
    print(table)

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


def crawling_kyochon():

    results = []
    for sido1 in range(1,18):
    #for sido1 in range(1, 5):
        for sido2 in count(start=1):
        #for sido2 in range(2,20):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1,sido2)
            html = cw.crawling(url=url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class':'list'})
            tag_li = tag_ul.find('li')
            tag_a = tag_li.find('a')

            tag_dl = tag_a.findAll('dl')
            #print('%s : sucess for script execute [%s]' % (datetime.now(), tag_dl))


            for dl in tag_dl:
                strings = list(dl.strings)

                #print(strings.strip())
                try:
                    name = strings[1]
                    #print(name)
                    address = strings[3].strip()
                    sidogu = address.split()[:2]
                    results.append((name, address) + tuple(sidogu))
                except Exception as e:
                    name is None


        #print(results)

        #store

        table = pd.DataFrame(results, columns=['name','address','sido','gungu'])
        table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
        table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
        print(table)



        table.to_csv(
            '{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
            encoding='utf-8',
            mode='w',
            index=True)





def crawling_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    #첫 페이지 로딩
    wd = webdriver.Chrome('D:/bigdatastudy/chromedriver/chromedriver.exe')
    wd.get(url)
    time.sleep(5)
    #print(wd.page_source)

    results = []
    for page in count(start=1):
    #for page in range(1,2):
        #자바스크립트 실행
        script = 'store.getList(%d)' % page #버튼 클릭시 매장리스트 정보 불러오는 것
        wd.execute_script(script)
        print('%s : sucess for script execute [%s]' % (datetime.now(), script))
        time.sleep(5)

        #실행결과 HTML(rendering 된 HTML) 가져오기
        html = wd.page_source

        #parsing with bs4
        bs = BeautifulSoup(html,'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id':'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        #마지막 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]

            results.append((name,address) + tuple(sidogu))

    #print(results)

    #store
    table = pd.DataFrame(results,columns=['name','address','sido','gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v,v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/goobne_table.csv'.format(RESULT_DIRECTORY),
         encoding='utf-8',
         mode='w',
         index=True)


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
    crawling_kyochon()

    #goobne
    #crawling_goobne()




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
