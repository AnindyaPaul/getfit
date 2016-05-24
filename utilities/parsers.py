import xml.dom.minidom


def parse_user(response):
    username, email, password, picture, code, verified = None, None, None, None, None, None
    domTree = xml.dom.minidom.parseString(response)
    users = domTree.getElementsByTagName("object")
    for user in users:
        username = user.getAttribute("pk")
        fields = user.getElementsByTagName("field")
        for field in fields:
            if(field.getAttribute("name") == "email"):
                if len(field.childNodes) > 0:
                    email = field.childNodes[0].data
            if(field.getAttribute("name") == "password"):
                if len(field.childNodes) > 0:
                    password = field.childNodes[0].data
            if(field.getAttribute("name") == "picture"):
                if len(field.childNodes) > 0:
                    picture = field.childNodes[0].data
            if(field.getAttribute("name") == "code"):
                if len(field.childNodes) > 0:
                    code = field.childNodes[0].data
            if(field.getAttribute("name") == "verified"):
                if len(field.childNodes) > 0:
                    verified = field.childNodes[0].data
                
    return username, email, password, picture, code, verified

def parse_products(response):
    domTree = xml.dom.minidom.parseString(response)
    products = domTree.getElementsByTagName("object")
    
    cnt = 0
    lst = list()
    for product in products:
        dct = dict()
        dct["productid"] = product.getAttribute("pk")
        fields = product.getElementsByTagName("field")
        for field in fields:
            if(field.getAttribute("name") == "name"):
                if len(field.childNodes) > 0:
                    dct["name"] = field.childNodes[0].data
            if(field.getAttribute("name") == "category"):
                if len(field.childNodes) > 0:
                    dct["category"] = field.childNodes[0].data
            if(field.getAttribute("name") == "price"):
                if len(field.childNodes) > 0:
                    dct["price"] = field.childNodes[0].data
            if(field.getAttribute("name") == "count"):
                if len(field.childNodes) > 0:
                    cnt = int(field.childNodes[0].data)
                    dct["count"] = cnt
            if(field.getAttribute("name") == "discount"):
                if len(field.childNodes) > 0:
                    dct["discount"] = field.childNodes[0].data
            if(field.getAttribute("name") == "details"):
                if len(field.childNodes) > 0:
                    dct["details"] = field.childNodes[0].data
            if(field.getAttribute("name") == "image"):
                if len(field.childNodes) > 0:
                    dct["image"] = field.childNodes[0].data
            if(field.getAttribute("name") == "sold"):
                if len(field.childNodes) > 0:
                    dct["sold"] = field.childNodes[0].data
            
        if cnt > 0:
            lst.append(dct)
    
    return lst

def parse_product(response):
    domTree = xml.dom.minidom.parseString(response)
    products = domTree.getElementsByTagName("object")
    
    cnt = 0
    dct = dict()
    for product in products:
        dct["productid"] = product.getAttribute("pk")
        fields = product.getElementsByTagName("field")
        for field in fields:
            if(field.getAttribute("name") == "name"):
                if len(field.childNodes) > 0:
                    dct["name"] = field.childNodes[0].data
            if(field.getAttribute("name") == "category"):
                if len(field.childNodes) > 0:
                    dct["category"] = field.childNodes[0].data
            if(field.getAttribute("name") == "price"):
                if len(field.childNodes) > 0:
                    dct["price"] = field.childNodes[0].data
            if(field.getAttribute("name") == "count"):
                if len(field.childNodes) > 0:
                    cnt = int(field.childNodes[0].data)
                    dct["count"] = cnt
            if(field.getAttribute("name") == "discount"):
                if len(field.childNodes) > 0:
                    dct["discount"] = field.childNodes[0].data
            if(field.getAttribute("name") == "details"):
                if len(field.childNodes) > 0:
                    dct["details"] = field.childNodes[0].data
            if(field.getAttribute("name") == "image"):
                if len(field.childNodes) > 0:
                    dct["image"] = field.childNodes[0].data
            if(field.getAttribute("name") == "sold"):
                if len(field.childNodes) > 0:
                    dct["sold"] = field.childNodes[0].data

    return dct

def parse_reviews(response):
    domTree = xml.dom.minidom.parseString(response)
    reviews = domTree.getElementsByTagName("object")
    
    lst = list()
    for review in reviews:
        dct = dict()
        dct["reviewid"] = review.getAttribute("pk")
        fields = review.getElementsByTagName("field")
        for field in fields:
            if(field.getAttribute("name") == "username"):
                if len(field.childNodes) > 0:
                    dct["username"] = field.childNodes[0].data
            if(field.getAttribute("name") == "productid"):
                if len(field.childNodes) > 0:
                    dct["productid"] = field.childNodes[0].data
            if(field.getAttribute("name") == "details"):
                if len(field.childNodes) > 0:
                    dct["details"] = field.childNodes[0].data
            if(field.getAttribute("name") == "rating"):
                if len(field.childNodes) > 0:
                    dct["rating"] = field.childNodes[0].data
            
        lst.append(dct)
    
    return lst

def parse_carts(response):
    domTree = xml.dom.minidom.parseString(response)
    carts = domTree.getElementsByTagName("object")
    
    lst = list()
    for cart in carts:
        dct = dict()
        dct["cartid"] = cart.getAttribute('pk')
        fields = cart.getElementsByTagName('field')
        for field in fields:
            if(field.getAttribute("name") == "username"):
                if len(field.childNodes) > 0:
                    dct["username"] = field.childNodes[0].data
            if(field.getAttribute("name") == "productid"):
                if len(field.childNodes) > 0:
                    dct["productid"] = field.childNodes[0].data
            if(field.getAttribute("name") == "count"):
                if len(field.childNodes) > 0:
                    dct["count"] = field.childNodes[0].data
        lst.append(dct)
    return lst

def parse_orders(response):
    domTree = xml.dom.minidom.parseString(response)
    orders = domTree.getElementsByTagName("object")
    
    lst = list()
    for order in orders:
        dct = dict()
        fields = order.getElementsByTagName('field')
        for field in fields:
            if(field.getAttribute("name") == "productid"):
                if len(field.childNodes) > 0:
                    dct["productid"] = field.childNodes[0].data
            if(field.getAttribute("name") == "count"):
                if len(field.childNodes) > 0:
                    dct["count"] = field.childNodes[0].data
            if(field.getAttribute("name") == "orderid"):
                if len(field.childNodes) > 0:
                    dct["orderid"] = field.childNodes[0].data
            if(field.getAttribute("name") == "duedate"):
                if len(field.childNodes) > 0:
                    dct["duedate"] = field.childNodes[0].data
            if(field.getAttribute("name") == "contactno"):
                if len(field.childNodes) > 0:
                    dct["contactno"] = field.childNodes[0].data
            if(field.getAttribute("name") == "address"):
                if len(field.childNodes) > 0:
                    dct["address"] = field.childNodes[0].data
            if(field.getAttribute("name") == "amount"):
                if len(field.childNodes) > 0:
                    dct["amount"] = field.childNodes[0].data
            if(field.getAttribute("name") == "paymentmethod"):
                if len(field.childNodes) > 0:
                    dct["paymentmethod"] = field.childNodes[0].data
            if(field.getAttribute("name") == "paymentinfo"):
                if len(field.childNodes) > 0:
                    dct["paymentinfo"] = field.childNodes[0].data
        lst.append(dct)
    return lst

