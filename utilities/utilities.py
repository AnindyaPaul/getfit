import urllib
import urllib2


dbhost = "http://127.0.0.1:8081/"

def make_query(url, data):
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    response = response.read()
    return response