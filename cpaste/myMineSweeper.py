import json
import random


def printAll(nums):  # 打印二维数组的全部信息
    for i in nums:
        for j in i:
            print(j, end=' ')
        print(' ')
    print(' ')


class Minesweeper():
    def __init__(self, height=16, width=30, mines=99, x=0, y=0):
        # 默认大小 30*16 99雷 初始位置为 0，0
        self.height = height
        self.width = width
        self.total = height * width
        self.minesCnt = mines

        self.mines = [[0] * width for i in range(height)]
        self.map = ['$'] * self.minesCnt + ['*'] * (self.total - self.minesCnt - 1)
        random.shuffle(self.map)
        self.map = self.map[:x * width + y] + ['*'] + self.map[x * width + y:]  # 保证第一个不是雷
        self.map = [self.map[i * width:(i + 1) * width] for i in range(height)]

        with open('map.json', 'w') as f:
            json.dump(self.map, f)
        with open('mines.json', 'w') as f:
            json.dump(self.mines, f)
        with open('map.json', 'r') as f:
            # 读取demp.json文件内容
            m = json.load(f)
            printAll(m)

        Click1(x, y)


class Click1():
    def __init__(self, x, y):
        with open('map.json', 'r') as f:
            self.map = json.load(f)
        self.x = x;
        self.y = y
        self.height = len(self.map)
        self.width = len(self.map[0])

        if self.map[x][y] == '$':
            print("You lose!");
            return
        if self.map[x][y] != '*':  # 所选区域已被选
            return
        print('click on: (', x, ',', y, ')')

        self.dfs(x, y)
        with open('map.json', 'w') as f:
            json.dump(self.map, f)

    def dfs(self, xi, yi):
        if not (0 <= xi < self.height and 0 <= yi < self.width):
            return
        if self.map[xi][yi] != '*':
            return
        c = self.count(xi, yi)
        self.map[xi][yi] = str(c)  # 统一用 str 类型存储
        if c == 0:  # 当且仅当周围没有雷时可以继续搜索
            self.dfs(xi + 1, yi);
            self.dfs(xi - 1, yi)
            self.dfs(xi, yi + 1);
            self.dfs(xi, yi - 1)
            self.dfs(xi + 1, yi + 1);
            self.dfs(xi - 1, yi - 1)
            self.dfs(xi - 1, yi + 1);
            self.dfs(xi + 1, yi - 1)
        return

    def count(self, x, y):  # 记录雷的个数
        dire = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        ans = 0
        for i in dire:
            if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                ans += (self.map[x + i[0]][y + i[1]] == '$')
        return ans


class AIclick2():  # version 2.0 找出所有安全区域
    def __init__(self):
        with open('map.json', 'r') as f:  # json文件内容
            self.map = json.load(f)
        with open('mines.json', 'r') as f:
            self.mines = json.load(f)
        self.height = len(self.map)
        self.width = len(self.map[0])

        self.state = 0  # 判断地图是否更新
        for i in range(self.height):
            for j in range(self.width):
                self.click(i, j)

        while self.state != 0:  # 继续搜索至map不更新
            self.state = 0
            for i in range(self.height):
                for j in range(self.width):
                    self.click(i, j)
        with open('map.json', 'w') as f:  # 更新map
            json.dump(self.map, f)
        with open('mines.json', 'w') as f:  # 更新mine
            json.dump(self.mines, f)

    def click(self, x, y):  # 确定雷 并点击
        if not self.map[x][y].isdigit():
            return -1
        dire = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        ans0 = ans1 = 0  # 记录未选区域、确定雷的个数
        for i in dire:
            if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                ans0 += (0 if self.map[x + i[0]][y + i[1]].isdigit() else 1)  # 非数字则未选
                ans1 += self.mines[x + i[0]][y + i[1]]

        if ans0 != 0 and ans0 == int(self.map[x][y]):  # 可确定为雷
            for i in dire:
                if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                    if not self.map[x + i[0]][y + i[1]].isdigit():
                        if self.mines[x + i[0]][y + i[1]] == 0:
                            self.state = 1;
                            print(x, y, "有更新", x + i[0], y + i[1], "为雷")
                            self.mines[x + i[0]][y + i[1]] = 1
        elif ans1 != 0 and ans1 == int(self.map[x][y]):  # 点击安全区域
            print(x, y, '可以排雷')
            for i in dire:
                if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                    if self.map[x + i[0]][y + i[1]] == '*' and self.mines[x + i[0]][y + i[1]] == 0:
                        self.state = 1
                        Click1(x + i[0], y + i[1])
            with open('map.json', 'r') as f:  # 点击后重新获取地图
                self.map = json.load(f)
        else:
            return


class AIclick3():  # version 3.0 没有安全区域，计算最佳落点
    def __init__(self):
        with open('map.json', 'r') as f:  # json文件内容
            self.map = json.load(f)
        with open('mines.json', 'r') as f:
            self.mines = json.load(f)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.borders = []  # 记录连通边界
        self.probs = []  # 记录概率 与self.areas对应

    def getAreas(self):  # 分割连通边界
        # 先找出所有的不确定边界
        uncertain = [[0] * self.width for i in range(self.height)]
        dire = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].isdigit():  # 数字周围未选的非雷区域
                    for x, y in dire:
                        if 0 <= x + i < self.height and 0 <= y + j < self.width:
                            if (not self.map[i + x][j + y].isdigit()) and self.mines[i + x][j + y] == 0:
                                uncertain[i + x][j + y] = 1
        printAll(uncertain)

        # 将连通的不确定边界加入self.borders, use dfs
        def dfs(ii, jj):
            if uncertain[ii][jj] == 0:
                return []
            ret = [[ii, jj]]
            uncertain[ii][jj] = 0
            for x, y in ((1, 0), (0, -1), (-1, 0), (0, 1)):
                if 0 <= x + ii < self.height and 0 <= y + jj < self.width:
                    ret += dfs(x + ii, y + jj)
            return ret

        for i in range(self.height):
            for j in range(self.width):
                if uncertain[i][j] == 1:
                    self.borders.append(dfs(i, j))
        print(self.borders)
        return

    def calcProb(self):
        return

    def click(self):
        return


if __name__ == '__main__':
    print("height,width,mines,x,y:")
    h, w, m, x, y = map(int, input().split())

    Minesweeper(h, w, m, x, y)
    print("Click on safe areas")
    c2 = AIclick2()
    # while c2.state:c2.click()

    # for i in range(int(input())):
    #     x,y,idx=map(int,input().split())
    #     Click1(x,y)

    print("No more safe areas, now calculate the probability")
    c3 = AIclick3()
    c3.getAreas()
    # while c3.state:c3.click()
