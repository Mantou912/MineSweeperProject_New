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

    def active(self):
        self.__connection = pymysql.connect(
            host=self.__host,
            user=self.__user,
            password=self.__password,
            database=self.__database,
        )
        self.__cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

    def inactive(self):
        self.__connection.close()
        self.__cursor.close()

    # -4 username错误
    def select_userInfo_clearCount(self, username) -> int:
        self.__connection.ping(reconnect=True)
        sql = "select clearCount from userInfo where username = '%s'" % username
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret is None:
            return -4
        else:
            return ret["clearCount"]

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

    def select_userInfo_boomCount(self, username) -> int:
        self.__connection.ping(reconnect=True)
        sql = "select boomCount from userInfo where username = '%s'" % username
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret is None:
            return -4
        else:
            return ret["boomCount"]

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
        self.__connection.ping(reconnect=True)
        sql = f"select * from userInfo where username = '{username}'"
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()

    def get_totalRank_data(self) -> Optional[List[dict]]:
        self.__connection.ping(reconnect=True)
        sql = "select username, clearCount, boomCount from userInfo"
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def clearData(self):
        self.__connection.ping(reconnect=True)
        sql = f"update userInfo set clearCount=0,boomCount=0"
        self.__cursor.execute(sql)
