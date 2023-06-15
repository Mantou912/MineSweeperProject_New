import json
import random
from collections import defaultdict
from fractions import Fraction

from flask import Flask, request
from flask_cors import CORS
from flask_mandrill import Mandrill

app = Flask(__name__)
app.config['MANDRILL_API_KEY'] = '...'
app.config['MANDRILL_DEFAULT_FROM'] = '...'
app.config['QOLD_SUPPORT_EMAIL'] = '...'
app.config['CORS_HEADERS'] = 'Content-Type'

mandrill = Mandrill(app)
CORS(app, supports_credentials=True)


def method_t():
    # with open('map.json', 'r') as f:  # json文件内容
    #     _map = json.load(f)
    # if sum(sum(j.isdigit() for j in i) for i in _map) == 0:
    #     return 0,0
    # else:
    #     c2 = AIclick2()
    #     c2.click()
    #     if c2.state == 0:
    #         c3 = AIclick3()
    #         c3.click()
    #     return 1,1
    return 1, 1


# 只接受get方法访问
@app.route("/", methods=["GET"])
def check():
    x, y = method_t()
    return_dict = {'x': x, 'y': y}
    # 判断输入参数是否为null
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/test_01", methods=["POST"])
def check_1():
    # 默认返回内容
    return_dict = {'return_code': '200', 'return_info': '处理成功', 'result': False}
    # 判断传入的json数据是否为空
    if request.get_data() is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = '请求参数为空'
        return json.dumps(return_dict, ensure_ascii=False)
    # 获取传入的参数
    get_Data = request.get_data()
    # 传入的参数为bytes类型，需要转化成json
    get_Data = json.loads(get_Data)
    name = get_Data.get('name')
    age = get_Data.get('age')
    # 对参数进行操作
    # return_dict['result'] = tt(name, age)

    return json.dumps(return_dict, ensure_ascii=False)


def printAll(nums):  # 打印二维数组的全部信息
    for i in nums:
        for j in i:
            print(j, end=' ')
        print(' ')
    print(' ')


class MineSweeper():
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

        Click1(x, y)


class Click1():
    def __init__(self, x, y):
        with open('click.json', 'w') as f:
            json.dump({'x': x, 'y': y}, f)
        with open('map.json', 'r') as f:
            self.map = json.load(f)
        self.x = x;
        self.y = y
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.lose = 0

        if self.map[x][y] == '$':
            print("You lose!", x, y, "is a mine")
            printAll(self.map)
            self.lose = 1
            return
        if self.map[x][y] != '*':  # 所选区域已被选
            return
        print('click on: (', x, ',', y, ')')

        self.dfs(x, y)
        # printAll(self.map)
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
        self.victory = 1  # 判断游戏胜利
        for i in self.map:
            if '*' in i:
                self.victory = 0
        if self.victory == 1:
            print("Victory")

        # while self.state!=0:  # 继续搜索至map不更新
        #     self.state=0
        #     for i in range(self.height):
        #         for j in range(self.width):
        #             self.click(i, j)

    def autoClick(self, x, y):  # 确定雷 并点击
        if not '0' <= self.map[x][y] <= '8':
            return
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
                            # print(x,y,"有更新",x+i[0],y+i[1],"为雷")
                            self.mines[x + i[0]][y + i[1]] = 1
        elif ans1 != 0 and ans1 == int(self.map[x][y]):  # 点击安全区域
            # print(x,y,'可以排雷')
            for i in dire:
                if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                    if self.map[x + i[0]][y + i[1]] == '*' and self.mines[x + i[0]][y + i[1]] == 0:
                        self.state = 1
                        Click1(x + i[0], y + i[1]);
                        break
        with open('map.json', 'r') as f:  # 点击后重新获取地图
            self.map = json.load(f)
        with open('mines.json', 'w') as f:  # 更新mine
            json.dump(self.mines, f)

    def click(self):
        for i in range(self.height):
            for j in range(self.width):
                self.autoClick(i, j)
                if self.state: break
            if self.state: break

        printAll(self.map)
        printAll(self.mines)
        with open('map.json', 'w') as f:  # 更新map
            json.dump(self.map, f)
        with open('mines.json', 'w') as f:  # 更新mine
            json.dump(self.mines, f)


class AIclick3():  # version 3.0 没有安全区域，计算最佳落点
    def __init__(self):
        with open('map.json', 'r') as f:  # json文件内容
            self.map = json.load(f)
        with open('mines.json', 'r') as f:
            self.mines = json.load(f)
        # 记录剩余雷数
        self.minesLeft = sum(i.count('$') for i in self.map) - sum(sum(i) for i in self.mines)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.uncertain = [[0] * self.width for i in range(self.height)]
        self.borders = []  # 记录连通边界
        self.probs = []  # 记录概率 与self.areas对应
        self.lose = 0  # 此方法可能踩雷
        self.minMines = 0  # 记录雷的最小数量

    def getAreas(self):  # 分割连通边界
        # 先找出所有的不确定边界
        parent = [[[-1, -1]] * self.width for i in range(self.height)]
        dire = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].isdigit():  # 数字周围未选的非雷区域
                    for x, y in dire:
                        if 0 <= x + i < self.height and 0 <= y + j < self.width:
                            if (not self.map[i + x][j + y].isdigit()) and self.mines[i + x][j + y] == 0:
                                self.uncertain[i + x][j + y] = 1
                                parent[i + x][j + y] = [i + x, j + y]  # 初始化根节点的父亲设为自己

        # print('parent self,uncertain:')
        # printAll(parent)
        # printAll(self.uncertain)

        # # 将连通的不确定边界加入self.borders, use dfs
        # def dfs(ii,jj):
        #     if visited[ii][jj]==0:
        #         return []
        #     ret=[[ii,jj]]
        #     visited[ii][jj]=0  # 防止走回头路
        #     for x,y in ((1,0),(0,-1),(-1,0),(0,1)):
        #         if 0<=x+ii< self.height and 0 <= y + jj < self.width:
        #             ret+=dfs(x+ii,y+jj)
        #     return ret
        #
        # for i in range(self.height):
        #     for j in range(self.width):
        #         if visited[i][j]==1:
        #             self.borders.append(sorted(dfs(i,j)))
        # dfs does not always work, use Union-Find instead

        def find(x, y):  # return (x,y)
            if parent[x][y] != [x, y]:
                parent[x][y] = find(parent[x][y][0], parent[x][y][1])
            return parent[x][y]

        def union(x1, y1, x2, y2):
            parent[find(x1, y1)[0]][find(x1, y1)[1]] = find(x2, y2)

        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j].isdigit():
                    for k in range(8):
                        if 0 <= i + dire[k][0] < self.height and 0 <= j + dire[k][1] < self.width \
                                and self.uncertain[i + dire[k][0]][j + dire[k][1]] == 1:
                            for l in range(k + 1, 8):
                                if 0 <= i + dire[l][0] < self.height and 0 <= j + dire[l][1] < self.width \
                                        and self.uncertain[i + dire[l][0]][j + dire[l][1]] == 1:
                                    union(i + dire[k][0], j + dire[k][1], i + dire[l][0], j + dire[l][1])

        # print('parent self,uncertain: now')
        # printAll(parent)
        # printAll(self.uncertain)
        d = defaultdict(list)
        for i in range(self.height):
            for j in range(self.width):
                if parent[i][j] != [-1, -1]:
                    d[tuple(find(i, j))].append([i, j])
        # print(d)
        for i in d:
            self.probs.append(sorted(self.calcProb(d[i])))

    def countBin1(self, n):  # 统计二进制中1的个数 即单个连通的雷个数
        ans = 0
        while n:
            n = n & (n - 1)
            ans += 1
        return ans

    def calcProb(self, nums):  # 计算每个连通区域的概率
        # print("lens of nums:",len(nums),nums)
        # printAll(self.uncertain)
        # printAll(self.map)
        # nums like: [[0, 2], [1, 2], [2, 2], [3, 2]]
        total = 0
        len_nums = len(nums)
        cnt = [0] * len_nums  # 统计出现次数
        restrict = set()
        minMinesForNums = 10 ** 5

        def count(x, y):  # 记录不确定区域的个数
            dire = ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
            cnt = 0
            ans = []
            for i in dire:
                if 0 <= x + i[0] < self.height and 0 <= y + i[1] < self.width:
                    cnt += (self.mines[x + i[0]][y + i[1]] == 1)
                    if self.uncertain[x + i[0]][y + i[1]] == 1:
                        # ans.append((x + i[0],y + i[1]))
                        ans.append(nums.index([x + i[0], y + i[1]]))
            return tuple(sorted(ans) + [int(self.map[x][y]) - cnt])
            # only tuple can add into set

        for i, j in nums:
            for x, y in ((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)):
                if 0 <= x + i < self.height and 0 <= y + j < self.width:
                    if self.map[x + i][y + j].isdigit():
                        restrict.add(count(x + i, y + j))

        # restrict like [(0, 1, 2, 4, 7, 2), (1, 2, 3, 1), (2, 3, 1), (4, 7, 9, 1), (5, 6, 7, 8, 9, 2), (7, 9, 1)]
        # restrict 存储连通边界周围数字的雷数、区域(下标)
        restrict = sorted(list(restrict))
        # print('restrict1:',restrict)
        # 将 restrict 分解
        while 1:
            flag = 0
            for i in range(len(restrict)):
                for j in range(i + 1, len(restrict)):
                    if set(restrict[i][:-1]) == set(restrict[j][:-1]):
                        restrict.remove(restrict[i])
                        flag = 1;
                        break
                    if not set(restrict[i][:-1]) - set(restrict[j][:-1]):  # j>i
                        restrict[j] = list(set(restrict[j][:-1]) - set(restrict[i][:-1])) + [
                            restrict[j][-1] - restrict[i][-1]]
                        flag = 1

                    if not set(restrict[j][:-1]) - set(restrict[i][:-1]):  # i>j
                        restrict[i] = list(set(restrict[i][:-1]) - set(restrict[j][:-1])) + [
                            restrict[i][-1] - restrict[j][-1]]
                        flag = 1
                if flag == 1:
                    break
            if flag == 0:
                break

        # print('restrict:',restrict)
        # [[0, 2, 7, 2], [1, 0], (2, 3, 1), [4, 0], [8, 5, 6, 1], (7, 9, 1)]

        # 二进制枚举出所有可能，即下标 [1:] 中为1的个数为 [0]
        # 对于nums 有2^len(nums)种可能
        # for i in range(1<<len_nums):
        #     isValid=1
        #     for j in restrict:
        #         if j[-1]!=sum(i&(1<<k)!=0 for k in j[:-1]):
        #             isValid=0
        #             break
        #     if isValid==1:
        #         total+=1
        #         minMinesForNums=min(minMinesForNums,self.countBin1(i))
        #         # print(bin(i))
        #         for j in range(len_nums):
        #             if i&(1<<j):
        #                 cnt[j]+=1
        #     if total>100:
        #         break
        #   二进制枚举复杂度为O(2^n) 运行时间指数爆炸 已停用

        # 计算每个区域概率 （Fraction）
        for i in restrict:
            self.minMines += i[-1]
            for j in i[:-1]:
                cnt[j] += Fraction(i[-1], len(i) - 1)

        return [(cnt[i], nums[i]) for i in range(len_nums)]

    def click(self):
        self.getAreas()
        # print("self.probs:",self.probs)

        # 找出连通边界中雷概率最低的点 与图中其他未选区域比较
        minPorb, x, y = 10, 0, 0
        for i in self.probs:
            if i[0][0] < minPorb:
                minPorb, x, y = i[0][0], i[0][1][0], i[0][1][1]

        otherAreas = 0
        ox, oy = 0, 0
        for i in range(self.height):
            for j in range(self.width):
                if (not self.map[i][j].isdigit()) and self.uncertain[i][j] == 0 and self.mines[i][j] == 0:
                    otherAreas += 1
                    ox, oy = i, j
        if otherAreas > 0 and self.minesLeft - self.minMines >= 0:
            otherPorb = Fraction(self.minesLeft - self.minMines, otherAreas)  # 其他未选区域的雷概率
        else:
            otherPorb = 10
        # print(minPorb,x,y,otherPorb)
        if minPorb <= otherPorb:
            c1 = Click1(x, y)
        else:
            c1 = Click1(ox, oy)
        if c1.lose == 1:
            self.lose = 1
        return


if __name__ == '__main__':
    CORS(app, resources=r'/*', supports_credentials=True)
