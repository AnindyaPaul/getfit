from django.shortcuts import render

from utilities.utilities import make_query, dbhost
from utilities.parsers import parse_products
from django.http.response import HttpResponse


# Create your views here.
def shop(request):
    
    products = list()
    if 'category' in request.GET:
        data = { 'category': request.GET['category'] }
        products = make_query(dbhost + "get_products_by_category/", data)
        products = parse_products(products)
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
        dct["origprice"] = product["price"]
        dct["discprice"] = float(product["price"]) * (100.0 - float(product["discount"])) / 100.0
        dct["details"] = product["details"]
        dct["image"] = product["image"]
        data.append(dct)
        cnt += 1
    #return HttpResponse(cnt)
    
    return render(request, "shop.html", { 'products': data })