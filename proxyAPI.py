from flask import Flask
from redisConn import RedisOpt
import random

app = Flask(__name__)
DBConn = RedisOpt()
__all__ =[app,]

@app.route('/')
def index():
    resp =  "welcome to my Proxies"
    return resp

@app.route('/getProxy')
def getProxy():
    proxies = DBConn.aliveProxy()
    proxy = random.choice(proxies)
    return proxy

@app.route('/getProxies/<num>')
def getProxies(num):
    proxies = DBConn.aliveProxy()
    if len(proxies) > int(num):
        temp = random.sample(proxies, int(num))
    else:
        temp = proxies
    resp = ''
    for proxy in temp:
        proxy = bytes.decode(proxy)
        resp += proxy + ','
    return resp.strip(',')

@app.route('/total')
def total():
    return str(len(DBConn.aliveProxy()))

if __name__ == "__main__":
    app.run(debug=True)