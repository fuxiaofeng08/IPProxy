from CheckIP import Check #检查IP可用性
from DownIP import ProxySpider #IP爬虫程序
import threading
import queue
import time
from redisConn import RedisOpt
from setting import *



class Crawl():
    def __init__(self):
        self.urls = self.CetPrxoy()
        self.urlQ = queue.Queue()
        self.proxies = {}
        self.lock = threading.Lock()
        self.redis = RedisOpt()
        self.optRedis= RedisOpt()

    def send(self):
        for url in self.urls:
            self.urlQ.put(url)
        print(">>", self.urlQ.qsize())

    # 去除队列中的proxy验证isAlive
    def isAlive(self):
        urlQ = self.urlQ
        global lock
        while True:
            if urlQ.empty():
                print(">线程%s运行结束"%threading.current_thread().name)
                break
            proxy = urlQ.get()
            flag = Check('http://' + proxy)
            self.lock.acquire()
            item = {}
            if flag:
                print("Get {} IsAlive~".format(proxy))
                item[proxy] = 100
            else:
                item[proxy] = 99
            self.optRedis.addProxy(item)
            self.lock.release()

    # 创建多线程调用isAlive函数
    def MuiltThread(self):
        l = []
        for i in range(MAX_THREAD):
            t = threading.Thread(target=self.isAlive, name=str(i+1))
            t.setDaemon(True)
            t.start()
            l.append(t)
        for t in l:
            t.join()
        print(">所有进程运行结束")

    # 获取IP代理网站IP、port，存入
    def CetPrxoy(self):
        spider = ProxySpider()
        spider.run()
        urls = spider.urls
        return urls

    def run(self):
        begin = time.time()
        print("Judge The Proxies IsAlive And Store Process Starting~")
        self.send()
        self.MuiltThread()
        # print(len(self.proxies.keys()))

        # self.optRedis.addProxy(self.proxies)
        end = time.time()
        print("Judge The Proxies IsAlive And Store Process Over~")
        print("Total Time>>",end-begin)


if __name__ == "__main__":
    Crawl = Crawl()
    Crawl.run()


