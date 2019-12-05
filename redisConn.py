from redis import ConnectionPool, StrictRedis
from setting import *

class RedisOpt():
    # 连接redis数据库
    def __init__(self):
        pool = ConnectionPool(host=HOST, port=PORT, db=0, password=PASSWORD)
        # 由于redis输出数据类型是bytes，所以连接配置提供decode_responses选项，可以选择直接输出str类型数据
        self.redis = StrictRedis(connection_pool=pool, decode_responses=True)

    # 添加proxy
    def addProxy(self, proxy):
        self.redis.zadd(DBNAME, proxy)

    # 删除proxy
    def remProxy(self, proxy):
        self.redis.zrem(DBNAME, proxy)

    # 获取指定排名区间proxy（start，end）
    def getProxy(self, start, end):
        return self.redis.zrevrange(DBNAME, start, end, withscores=False)

    #获取有效proxy，即分数等于100
    def aliveProxy(self):
        return self.redis.zrevrangebyscore(DBNAME, 100, 100)

    # 更改proxy分数
    def updateProxy(self,proxy):
        newScore = self.redis.zincrby(DBNAME, -1, proxy)
        if newScore <= 90:
            print(proxy,'被移除')
            self.remProxy(proxy)

    # 获取redis中Proxy的个数
    def lenProxy(self):
        return self.redis.zcard(DBNAME)

if __name__ == "__main__":
    redisOpt = RedisOpt()
    tmp = {'zhang':55,'wang':55}
    redisOpt.addProxy(tmp)
    redisOpt.updateProxy('zhang')

