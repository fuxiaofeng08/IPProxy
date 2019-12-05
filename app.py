from setting import *
from CheckProxies import CheckProxy
from StoreIP import Crawl
from proxyAPI import app as flask_app
import time
import threading


def Crawler():
    while True:
        time.sleep(CrawlTime)
        crawl = Crawl()
        crawl.run()

def Updater():
    while True:
        time.sleep(UpdateTime)
        update = CheckProxy()
        update.run()


def FlaskRun():
    flask_app.run(host=SERVERHOST, port=SERVERPORT)

def run():
    crawlThread = threading.Thread(target=Crawler)
    updateThread = threading.Thread(target=Updater)
    flaskThread = threading.Thread(target=FlaskRun)
    crawlThread.start()
    updateThread.start()
    flaskThread.start()
    crawlThread.join()
    updateThread.join()
    flaskThread.join()

if __name__ == '__main__':
    run()



