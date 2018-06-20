
import collection.crawler as cw

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

