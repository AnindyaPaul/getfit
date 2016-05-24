from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from utilities.parsers import parse_products, parse_product, parse_reviews, parse_user, parse_carts
from utilities.utilities import make_query, dbhost
from accounts.views import enter, profile
from datetime import datetime, timedelta


# Create your views here.
def shop(request):
    
    category = None
    products = list()
    if 'category' in request.GET:
        data = { 'category': request.GET['category'] }
        products = make_query(dbhost + "get_products_by_category/", data)
        products = parse_products(products)
        category = request.GET['category']
    else:
        data = dict()
        products = make_query(dbhost + "get_products/", data)
        products = parse_products(products)
    
    data = list()
    cnt = 0
    for product in products:
        dct = dict()
        # productid, name, category, price, count, discount, details, image, sold 
        dct["productid"] = product["productid"]
        dct["name"] = product["name"]
        dct["category"] = product["category"]
        dct["discprice"] = float(product["price"]) * (100.0 - float(product["discount"])) / 100.0
        if dct["discprice"] != float(product["price"]):
            dct["origprice"] = product["price"]
        dct["details"] = product["details"]
        dct["image"] = product["image"]
        
        reviews = make_query(dbhost + "get_reviews/", {'productid': product['productid']})
        reviews = parse_reviews(reviews)
        
        cnt = 0.0
        rating = 0.0
        for review in reviews:
            rating += float(review["rating"])
            cnt += 1.0
        if cnt>0 :
            rating = rating/cnt
        
        dct['rating'] = rating
        data.append(dct)
        cnt += 1
    #return HttpResponse(cnt)
    
    if category is None:
        return render(request, "shop.html", { 'products': data })
    else:
        return render(request, "shop.html", { 'products': data, 'category': category })

def product(request):

    if 'productid' not in request.GET:
        return HttpResponseRedirect(reverse(shop))
    
    data = { 'productid': request.GET['productid'] }
    product = make_query(dbhost + "get_product/", data)
    product = parse_product(product)

    dct = dict()
    # productid, name, category, price, count, discount, details, image, sold 
    dct["productid"] = product["productid"]
    dct["name"] = product["name"]
    dct["category"] = product["category"]
    dct["discprice"] = float(product["price"]) * (100.0 - float(product["discount"])) / 100.0
    if dct["discprice"] != float(product["price"]):
        dct["origprice"] = product["price"]
    dct["details"] = product["details"]
    dct["image"] = product["image"]

    reviews = make_query(dbhost + "get_reviews/", data)
    reviews = parse_reviews(reviews)

    rating = 0.0
    cnt = 0.0
    data = list()
    for review in reviews:
        dct2 = dict()
        dct2["productid"] = review["productid"]
        dct2["username"] = review["username"]
        
        temp = { 'username': review["username"] }
        response = make_query(dbhost + "get_user/", temp)
        _, _, _, picture, _,_ = parse_user(response)
        dct2["image"] = picture
        
        dct2["reviewid"] = review["reviewid"]
        dct2["rating"] = review["rating"]
        rating += float(review["rating"])
        cnt += 1.0
        dct2["details"] = review["details"]
        data.append(dct2)
    
    if cnt>0 :
        rating = rating/cnt

    dct['rating'] = str(rating)
    
    return render(request,"product.html", { 'product': dct , 'reviews':data })

def add_review(request):
    
    dct = dict()
    dct['productid'] = request.POST['productid']
    
    if 'username' in request.POST:
        
        if request.POST['username'] == request.session['username']:
            
            if request.POST['rating'] != "" and request.POST['details'] != "": 
                
                dct['username'] = request.POST['username']
                dct['productid'] = request.POST['productid']
                dct['details'] = request.POST['details']
                dct['rating'] = request.POST['rating']
                review = make_query(dbhost + "set_review/", dct)

    return HttpResponseRedirect("/product/?productid=" + request.POST['productid'])

def cart(request):
    if 'username' not in request.session:
        return HttpResponseRedirect(reverse(enter))
    
    username = request.session['username']
    data = { 'username': username }
    carts = make_query(dbhost + "get_carts/", data)
    carts = parse_carts(carts)
    
    total = 0.0
    lst = list()
    for cart in carts:
        data = { 'productid': cart['productid'] }
        product = make_query(dbhost + "get_product/", data)
        product = parse_product(product)
        
        dct = dict()
        dct['uprice'] = float(product["price"]) * (100.0 - float(product["discount"])) / 100.0
        dct['tprice'] = dct['uprice'] * float(cart['count'])
        total += dct['tprice']
        dct['productid'] = cart['productid']
        dct['productname'] = product['name']
        dct['count'] = int(cart['count'])
        lst.append(dct)       

    return render(request, "cart.html", { 'carts': lst, 'total': total })

def add_to_cart(request):
    if 'username' not in request.session:
        return HttpResponseRedirect("/product/?productid=" + request.POST['productid'])
    
    username = request.session['username']
    productid = request.POST['productid']
    count = int(request.POST['count'])
    data = { 'username':username, 'productid':productid, 'count':count }
    response = make_query(dbhost + "set_cart/", data)
    return HttpResponseRedirect("/product/?productid=" + request.POST['productid'])

def checkout(request):
    return render(request, 'checkout.html')

def place_order(request):
    
    username = request.session['username']
    contactno = request.POST.get('contactno')
    address = request.POST.get('address')
    orderid = datetime.today()
    duedate = orderid + timedelta(days=14)
    duedate = duedate.date()
    paymentmethod = request.POST.get('optradio')
    paymentinfo = None
    if 'paymentinfo' in request.POST:
        paymentinfo = request.POST['paymentinfo']

    data = { 'username': username }
    carts = make_query(dbhost + "get_carts/", data)
    carts = parse_carts(carts)
    
    for cart in carts:
        productid = cart['productid']
        cartcount = int(cart['count'])
        
        product = make_query(dbhost + "get_product/", {'productid': productid})
        product = parse_product(product)
        avalcount = int(product['count'])
        amount = float(product["price"]) * (100.0 - float(product["discount"])) / 100.0
        
        if cartcount > avalcount:
            # handle more than available order
            return HttpResponseRedirect("cart")

        product['count'] = int(product['count']) - cartcount
        product['sold'] = int(product['sold']) + cartcount
        response = make_query(dbhost + "set_product/", product)

        data = dict()
        data['username'] = username
        data['productid'] = productid
        data['count'] = cartcount
        data['delivstatus'] = "Pending"
        data['orderid'] = str(orderid)
        data['duedate'] = str(duedate)
        data['contactno'] = contactno
        data['address'] = address
        data['amount'] = amount
        data['paymentmethod'] = paymentmethod
        data['paymentinfo'] = paymentinfo

        response = make_query(dbhost + "set_order/", data)
    
    data = { 'username': username }
    carts = make_query(dbhost + "del_carts/", data)
    
    return HttpResponseRedirect(reverse(profile))





