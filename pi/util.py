from urllib import request


def get_ip():
    return request.urlopen('https://api.ipify.org').read().decode('utf8')