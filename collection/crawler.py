
import sys
from urllib.request import Request,urlopen
from datetime import datetime

#def error(e):
#    print('%s : %s' % (e.datetime.now()),file=sys.stderr)


def crawling(
        url='',
        encoding = 'utf-8',
        proc = lambda html: html, #통과코드
        store=lambda html: html,
        err=lambda e: print('%s : %s' % (e.datetime.now()),file=sys.stderr)):
    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            result = receive.decode(encoding) #리시브에 디코드된 결과를 result에
            result = store(proc(result)) #proc으로 html 리턴
            """
            if store is not None: #store = None일떄
                result = store(result)
            if proc is not None:
                result = proc(result)
            """
        except UnicodeDecodeError:
            result = receive.decode(encoding,'replace')

        return result


    except Exception as e:
        err(e)
        #print('%s : %s' % (e.datetime.now()),file=sys.stderr)