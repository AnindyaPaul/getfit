import random
import urllib
import urllib2

from django.contrib.auth.hashers import check_password, make_password
from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "index.html")

def enter(request):
    return render(request, "enter.html")

def signout(request):
    request.session.flush()
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        url = "http://127.0.0.1:8081/user_exists/"
        data = {'username':username}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()
        if(response == "1"):
            data = {'status':'1'}  # error
            return render(request, "enter.html", data)

        url = "http://127.0.0.1:8081/store_user/"
        code = random.randint(10000, 100000000)
        code = str(code)
        password = make_password(password)
        data = {'username':username, 'password':password, 'email':email, 'code':code}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()

        data = {'username':username}
        return render(request, "verify.html", data)
        
    return HttpResponse("Error!!!")

def verify(request):
    
    if request.method == 'POST':

        username = request.POST['username']
        code = request.POST['token']

        url = "http://127.0.0.1:8081/get_code/"
        data = {'username':username }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()
        
        if(response == code):
            request.session['username'] = username
            url = "http://127.0.0.1:8081/make_verify/"
            data = {'username':username }
            data = urllib.urlencode(data)
            req = urllib2.Request(url, data)
            response = urllib2.urlopen(req)
            response = response.read()
            return render(request, "index.html")
        
        else:
            data = {'username': username, 'status':'1'}  # error
            return render(request, "verify.html", data)


def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        url = "http://127.0.0.1:8081/user_exists/"
        data = {'username':username}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()
        if(response == "0"):
            data = {'status':'1'}  # error
            return render(request, "enter.html", data)

        url = "http://127.0.0.1:8081/is_verified/"
        data = {'username':username}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()

        if(response == "0"):  # not verified
            data = {'username':username}
            return render(request, "verify.html", data)


                                            # verified
        url = "http://127.0.0.1:8081/get_password/"
        data = {'username':username }
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)
        response = response.read()
        if check_password(password, response):
            request.session['username'] = username
        else:
            data = {'status':'1'}  # error
            return render(request, "index.html", data)

        return render(request, "index.html")
