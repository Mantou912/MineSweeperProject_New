import time
from typing import List
from typing import Tuple

from .mineSweeper import ClearMine
from .database import sqlOperator


class Server:
    def __init__(self) -> None:
        self.__CM = ClearMine()
        self.__SQL = sqlOperator()
        self.__SQL.active()
        self.__ready = 0

    def login(self, username: str, password: str) -> bool:
        self.__SQL.clearData()
        """用于用户登录时,判断收到的账号密码是否匹配"""
        data = self.__SQL.select_by_user(username)
        if data is None:
            return False
        return password == data["passwd"]

    def click(self, x: int, y: int, username: str) -> Tuple[bool, str, bool, int]:
        color_number = self.__CM.get_user_color_num(username)
        color_string = self.__CM.get_user_color_str(color_number)
        click_status = self.__CM.click(x, y, username)
        finish = self.__CM.judge_win()

        bool_ret = False
        if click_status >= 0:
            clearCount = self.__SQL.select_userInfo_clearCount(username)
            self.__SQL.update_userInfo_clearCount(username, clearCount + click_status)
            bool_ret = True
        elif click_status == -1:
            boomCount = self.__SQL.select_userInfo_boomCount(username)
            self.__SQL.update_userInfo_boomCount(username, boomCount + 1)
            bool_ret = True
        # 返回 有效点击 color 结束 点击时间
        return bool_ret, color_string, finish, self.__CM.get_timmer()

    def timmer(self) -> int:
        # 时间
        return self.__CM.get_timmer()

    def history(self) -> List[Tuple[int, int, str]]:
        # 历史
        return self.__CM.get_click_history()

    def args(self) -> dict:
        # 地图数据
        return self.__CM.get_args()

    def restart(self, waitTime=-5) -> None:
        # 重启
        self.__ready = time.time() + waitTime
        self.__CM.restart(True)

    def ready(self) -> bool:
        # ready
        return time.time() > self.__ready

    def give_color(self, username: str) -> None:
        # 分配颜色
        self.__CM.give_color(username)

    def rank(self) -> dict:
        # 本局排名
        return self.__CM.get_rank()

    def total_rank(self) -> List[dict]:
        """查询历史积累战绩"""
        return self.__SQL.get_totalRank_data()
