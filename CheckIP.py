import requests
from setting import HEADERS

def Check(proxy):
    proxies = {"http": proxy}
    try:
        resp = requests.get(url="http://www.baidu.com", headers=HEADERS, proxies=proxies, timeout=1.5)
        if resp.status_code == 200:
            return True
        else:
            return False
    except:
        return False

if __name__ == "__main__":
    if Check('187.16.4.121:8080'):
        print("Proxy 可用")
    else:
        print("Proxy 不可用")
