import pymysql
from DBUtils.PooledDB import PooledDB
from cscd_spider import db_config as config

'''
@功能：PT数据库连接池
'''


class DBConnectionPool(object):
    __pool = None

    def __enter__(self):
        self.conn = self.getConn()
        self.cursor = self.conn.cursor()
        return self

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=config.DB_MIN_CACHED, maxcached=config.DB_MAX_CACHED,
                                   maxshared=config.DB_MAX_SHARED, maxconnections=config.DB_MAX_CONNECYIONS,
                                   blocking=config.DB_BLOCKING, maxusage=config.DB_MAX_USAGE,
                                   setsession=config.DB_SET_SESSION,
                                   host=config.DB_TEST_HOST, port=config.DB_TEST_PORT,
                                   user=config.DB_TEST_USER, passwd=config.DB_TEST_PASSWORD,
                                   db=config.DB_TEST_DBNAME, use_unicode=False, charset=config.DB_CHARSET)

        return self.__pool.connection()

    """
    @summary: 释放连接池资源
    """

    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()


'''
@功能：获取PT数据库连接
'''


def get_db_connect():
    return DBConnectionPool()
