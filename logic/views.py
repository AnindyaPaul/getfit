import random
import urllib
import urllib2

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from logic.parsers import parse_user


# Create your views here.
dbhost = "http://127.0.0.1:8081/"

def index(request):
    return render(request, "index.html")

def enter(request):
    return render(request, "enter.html")

def signout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse(index))

def signup(request):
    
    username = request.POST['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, _, _, _, _, _ = parse_user(response)
    
    if(username is not None):
        return HttpResponseRedirect(reverse(index))

    username = request.POST['username']
    email = request.POST['email']
    password = make_password(request.POST['password'])
    code = genCode()
    verified = "0"
    data = {'username': username, 'email':email, 'password':password, 'code':code, 'verified': verified}
    response = make_query(dbhost + "set_user/", data)
    
    msg = 'Your verification code is: ' + code
    send_mail('Verification code', msg, 'getfitwebproject@gmail.com', [email], fail_silently=True)

    data = {'username': username }
    return render(request, "verify.html", data)

def verify(request):
    
    username = request.POST['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, password, _, code, _ = parse_user(response)
    
    if(code == request.POST['code']):
        request.session['username'] = username
        data = {'username': username, 'email': email, 'password':password, 'code':code, 'verified':"1"}
        response = make_query(dbhost + "set_user/", data)
        return HttpResponseRedirect(reverse(index))
    
    else:
        data = {'username': username}  # error
        return render(request, "verify.html", data)

def signin(request):

    username = request.POST['username']

    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, _, password, _, _, verified = parse_user(response)
    
    if(username is None):
        return HttpResponseRedirect(reverse(enter))

    if(verified == "0"):
        data = {'username':username}
        return render(request, "verify.html", data)

    if check_password(request.POST['password'], password):
        request.session['username'] = username

    return HttpResponseRedirect(reverse(index))

def make_query(url, data):
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    response = response.read()
    return response

def genCode():
    return str(random.randint(10000, 100000000))