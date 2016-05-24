from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from utilities.parsers import parse_products, parse_product, parse_reviews, parse_user
from utilities.utilities import make_query, dbhost


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
        data.append(dct)
        cnt += 1
    #return HttpResponse(cnt)
    
    if category is None:
        return render(request, "shop.html", { 'products': data })
    else:
        return render(request, "shop.html", { 'products': data, 'category': category })

def product(request):

    if 'productid' in request.GET:
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
    
    else:
        return HttpResponseRedirect(reverse(shop))

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
    return render(request, "cart.html")