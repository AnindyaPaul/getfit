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



