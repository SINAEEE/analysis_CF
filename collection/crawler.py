
import sys
from urllib.request import Request,urlopen
from datetime import datetime



def crawling(
        url='',
        encoding = 'utf-8'):
    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            result = receive.decode(encoding)
        except UnicodeDecodeError:
            result = receive.decode(encoding,'replace')

        return result


    except Exception as e:
        print('%s : %s' % (e.datetime.now()),file=sys.stderr)