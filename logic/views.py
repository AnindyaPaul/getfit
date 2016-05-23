import os
import random
import urllib
import urllib2

from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from getfit import settings
from logic.parsers import parse_user


# Create your views here.
dbhost = "http://127.0.0.1:8081/"

def make_query(url, data):
    data = urllib.urlencode(data)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    response = response.read()
    return response

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
    code = gencode()
    verified = "0"
    data = {'username': username, 'email':email, 'password':password, 'picture':None , 'code':code, 'verified': verified}
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
        data = {'username': username, 'email': email, 'password':password, 'picture':None, 'code':"0", 'verified':"1"}
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

def forgot(request):
    
    username = request.POST['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, password, picture, code, verified = parse_user(response)
    
    if(username is None):
        return HttpResponseRedirect(reverse(enter))
    
    code = gencode()
    msg = 'Visit: http://localhost:8080/pwdreset?code=' + code
    send_mail('Password reset', msg, 'getfitwebproject@gmail.com', [email], fail_silently=True)
    
    data = {'username': username, 'email': email, 'password':password, 'picture':picture, 'code':code, 'verified':verified}
    response = make_query(dbhost + "set_user/", data)
    
    return HttpResponseRedirect(reverse(index))

def pwdreset(request):
    code = request.GET['code']
    if(code =="0"):
        return HttpResponseRedirect(reverse(enter))
    
    data = { 'code': code }
    response = make_query(dbhost + "get_user_by_code/", data)
    username, _, _, _, _, _ = parse_user(response)
    
    if(username is None):
        return HttpResponseRedirect(reverse(enter))
    
    data = { 'username': username }
    return render(request, "newpwd.html", data)

def storepwd(request):
    username = request.POST['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, _, picture, _, _ = parse_user(response)
    
    password = make_password(request.POST['password'])
    data = {'username': username, 'email': email, 'password':password, 'picture':picture, 'code':"0", 'verified':"1"}
    response = make_query(dbhost + "set_user/", data)
    return HttpResponseRedirect(reverse(index))
    
def gencode():
    return str(random.randint(10000, 100000000))

def profile(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse(index))
    
    username = request.session['username']
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, _, picture, _, _ = parse_user(response)
    
    if picture is None:
        picture = "profilepic/default.jpg"
    
    data = { 'username': username, 'email': email, 'picture': picture}
    return render(request, 'profile.html', data)

def updprofile(request):
    username = request.session['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, password, picture, code, verified = parse_user(response)
    
    if request.POST['password'] != "":
        password = make_password(request.POST['password'])
    data = {'username': username, 'email': email, 'password':password, 'picture':picture, 'code':code, 'verified':verified}
    response = make_query(dbhost + "set_user/", data)
    
    return HttpResponseRedirect(reverse(profile))
    
    return HttpResponse('update')

def updprofilepic(request):
    username = request.session['username']
    
    if len(request.FILES) > 0:
        saveprofpic(username, request.FILES['picture'])
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, password, picture, code, verified = parse_user(response)
    
    picture = "profilepic/" + username + ".jpg"
    
    data = {'username': username, 'email': email, 'password':password, 'picture':picture, 'code':code, 'verified':verified}
    response = make_query(dbhost + "set_user/", data)
    
    return HttpResponseRedirect(reverse(profile))

def delprofilepic(request):
    username = request.session['username']
    
    data = { 'username': username }
    response = make_query(dbhost + "get_user/", data)
    username, email, password, picture, code, verified = parse_user(response)
    
    if picture is not None:
        os.remove(os.path.join(settings.MEDIA_ROOT, picture))
    
    picture = ""
    
    data = {'username': username, 'email': email, 'password':password, 'picture':picture, 'code':code, 'verified':verified}
    response = make_query(dbhost + "set_user/", data)
    
    return HttpResponseRedirect(reverse(profile))
    
def saveprofpic(username, f):
    with open(settings.MEDIA_ROOT + '/profilepic/' + username + '.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    
    


