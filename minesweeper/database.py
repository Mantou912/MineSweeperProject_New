from random import randint
from typing import Optional, List

import pymysql


class sqlOperator:
    def __init__(self, host='127.0.0.1', user='root', password='Mt369815..', database='minesweeper'):
        self.__cursor = None
        self.__connection = None
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database

    # 激活对象
    def active(self):
        self.__connection = pymysql.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database,
        )
        self.__cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭对象功能
    def inactive(self):
        self.__connection.close()
        self.__cursor.close()

    # 查询用户扫出的区域个数
    # -4表示username错误
    def select_userInfo_clearCount(self, username) -> int:
        self.__connection.ping(reconnect=True)
        sql = "select clearCount from userInfo where username = '%s'" % username
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret is None:
            return -4
        else:
            return ret["clearCount"]

    # 更新用户扫出的区域个数
    # -4表示username错误  运行正常返回1
    def update_userInfo_clearCount(self, username, clearCount) -> int:
        self.__connection.ping(reconnect=True)
        sql = "update userInfo set clearCount = %d where username= '%s'" % (
            clearCount,
            username,
        )
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -4
        else:
            return ret

    # 查询用户炸雷个数
    # -4表示username错误
    def select_userInfo_boomCount(self, username) -> int:
        self.__connection.ping(reconnect=True)
        sql = "select boomCount from userInfo where username = '%s'" % username
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret is None:
            return -4
        else:
            return ret["boomCount"]

    # 更新用户炸雷个数
    # -4表示username错误
    def update_userInfo_boomCount(self, username, boomCount):
        self.__connection.ping(reconnect=True)
        sql = "update userInfo set boomCount = %d where username= '%s'" % (
            boomCount,
            username,
        )
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -4
        else:
            return ret

    def select_by_user(self, username: str) -> Optional[dict]:
        """根据用户名查询匹配者的所有信息"""
        self.__connection.ping(reconnect=True)
        sql = f"select * from userInfo where username = '{username}'"
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()

    def get_totalRank_data(self) -> Optional[List[dict]]:
        """查询总榜(所有用户)信息"""
        self.__connection.ping(reconnect=True)
        sql = "select username, clearCount, boomCount from userInfo"
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()
