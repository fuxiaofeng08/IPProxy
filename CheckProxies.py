#CheckProxies.py
#验证redis数据库proxies可用性，可用score设置100，不可用当前score-1，低于90的proxy删除
from redisConn import RedisOpt
from queue import Queue
from CheckIP import Check
import threading

class CheckProxy():
    def __init__(self):
        self.opt = RedisOpt() #获取redis数据库的操作对象
        self.totalNum = 0
        self.queue = Queue()

    #获取redis数据库中Proxies的个数
    def getTotalNum(self):
        self.totalNum = self.opt.lenProxy()

    #获取每次取出Proxies的区间，并存入队列
    def getCheckNum(self):
        end = self.totalNum
        temp = self.opt.getProxy(0, end)
        for i in temp:
            self.queue.put(i)

    #获取redis数据库中proxies
    def getPoxies(self):
        while True:
            if self.queue.empty():
                print(threading.current_thread().name,'运行结束')
                break
            proxy= self.queue.get()
            proxy = bytes.decode(proxy)
            flag = Check(proxy)
            if flag:
                print(">%s< is alive"%proxy)
                self.opt.addProxy({proxy:100})
            else:
                self.opt.updateProxy(proxy)
    #执行程序run
    def run(self):
        print(">>Update Proxies Process Starting")
        self.getTotalNum()
        self.getCheckNum()
        l = []
        for i in range(30):
            t = threading.Thread(target=self.getPoxies, name='Thread' + str(i+1))
            t.setDaemon(True)
            t.start()
            l.append(t)
        for t in l:
            t.join()
        print(">>Update Proxies Process End")

if __name__ == "__main__":
    isAlive = CheckProxy()
    isAlive.run()















