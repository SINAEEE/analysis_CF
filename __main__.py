
from itertools import count
from bs4 import BeautifulSoup

import collection.crawler as cw

def crawling_pericana():
    results = []
    #for page in range(1,2):
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

    print(results)







if __name__ == '__main__':
    #pelicanas
    crawling_pericana()



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
