
import collection.crawler as cw

def my_error(e):
    print("my error : " +e)

result = cw.crawling(
    url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
    encoding='cp949')

print(result)
