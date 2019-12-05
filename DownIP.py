import requests
import time
from lxml import etree
import threading
from setting import *

class ProxySpider():
    def __init__(self):
        self.headers = HEADERS
        self.urls = []
        self.lock = threading.Lock()
        self.totalpage = TOTAL_PAGE

    def parasePage(self, url):
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.text
            else:
                return None
        except:
            print(">%s< Erro"%url)

    def BaJiuSpider(self):
        page = 1
        while page<self.totalpage:
            url = "http://www.89ip.cn/index_" + str(page) + ".html"
            print(">>Stating Crawl %s" % url)
            ProxyList = []
            respHtml = self.parasePage(url)
            if respHtml:
                resp = etree.HTML(respHtml)
                IPList = resp.xpath("//tbody/tr/td[1]/text()")
                PortList = resp.xpath("//tbody/tr/td[2]/text()")
                for ip, proxy in zip(IPList, PortList):
                    ipProxy = ip.strip() + ':' + proxy.strip()
                    ProxyList.append(ipProxy)
            page += 1
            self.lock.acquire()
            self.urls.extend(ProxyList)
            self.lock.release()
            time.sleep(1)

    def LiuLiuSpider(self):
        page = 1
        while page<self.totalpage:
            url = "http://www.66ip.cn/" + str(page) + ".html"
            print(">>Stating Crawl %s" % url)
            ProxyList = []
            respHtml = self.parasePage(url)
            if respHtml:
                resp = etree.HTML(respHtml)
                IPList = resp.xpath("//div[@id='main']//table//tr/td[1]/text()")[1:]
                PortList = resp.xpath("//div[@id='main']//table//tr/td[2]/text()")[1:]
                for ip, proxy in zip(IPList, PortList):
                    ipProxy = ip.strip() + ':' + proxy.strip()
                    ProxyList.append(ipProxy)
            page += 1
            self.lock.acquire()
            self.urls.extend(ProxyList)
            self.lock.release()
            time.sleep(1)

    def xiciSpider(self):
        page = 1
        while page<self.totalpage:
            url = "https://www.xicidaili.com/nt/" + str(page)
            print(">>Stating Crawl %s"%url)
            ProxyList = []
            respHtml = self.parasePage(url)
            if respHtml:
                resp = etree.HTML(respHtml)
                IPList = resp.xpath("//table[@id='ip_list']//tr/td[2]/text()")
                PortList = resp.xpath("//table[@id='ip_list']//tr/td[3]/text()")
                for ip, port in zip(IPList, PortList):
                    proxy = ip.strip() + ':' + port.strip()
                    ProxyList.append(proxy)
            page += 1
            self.lock.acquire()
            self.urls.extend(ProxyList)
            self.lock.release()
            time.sleep(1)

    def run(self):
        threads = []
        print(">>Crawl Proxies Process Starting~")
        fun = [self.BaJiuSpider, self.LiuLiuSpider(), self.xiciSpider]
        for i in range(len(fun)):
            t = threading.Thread(target=fun[i])
            t.setDaemon(True)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        print(">>Crawl Proxies Process Over~")


if __name__ == "__main__":
    ProxyList = ProxySpider()
    ProxyList.run()
    print(len(ProxyList.urls))