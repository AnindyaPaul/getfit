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