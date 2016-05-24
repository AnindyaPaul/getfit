"""getfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

import getfit
from accounts import views as accviews
from shop import views as shopviews


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', getfit.views.index,name='index'),
    
    url(r'^enter/',accviews.enter,name='enter'),
    url(r'^signin/',accviews.signin,name='signin'),
    url(r'^signup/',accviews.signup,name='signup'),
    url(r'^signout/',accviews.signout,name='signout'),
    url(r'^verify/',accviews.verify,name='verify'),
    url(r'^forgot/',accviews.forgot,name='forgot'),
    url(r'^pwdreset/',accviews.pwdreset,name='pwdreset'),
    url(r'^storepwd/',accviews.storepwd,name='storepwd'),
    
    url(r'^profile/',accviews.profile,name='profile'),
    url(r'^updprofile/',accviews.updprofile,name='updprofile'),
    url(r'^updprofilepic/',accviews.updprofilepic,name='updprofilepic'),
    url(r'^delprofilepic/',accviews.delprofilepic,name='delprofilepic'),
    
    url(r'^shop/',shopviews.shop,name='shop'),
    url(r'^product/',shopviews.product,name='product'),
]
