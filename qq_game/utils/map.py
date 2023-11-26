from argparse import Namespace

from utils.zobrist import Zobrist, HashTable
import copy


def convert_params(params):
    if type(params) is list:
        return [Namespace(**p) for p in params]
    return Namespace(**params)


# 用于估价函数中边角的计算
rnd = [{'s': 0, 'a': 1, 'b': 8, 'c': 9, 'dr': [1, 8]},
       {'s': 7, 'a': 6, 'b': 15, 'c': 14, 'dr': [-1, 8]},
       {'s': 56, 'a': 57, 'b': 48, 'c': 49, 'dr': [1, -8]},
       {'s': 63, 'a': 62, 'b': 55, 'c': 54, 'dr': [-1, -8]}
       ]
rnd = convert_params(rnd)

zobrist = Zobrist()


class Map():

    def __init__(self, map=None):
        if map:
            self.board = map.board
            self.side = map.side
            self.frontier = map.frontier
            return

        self.key = [0, 0]

        self.board = [0] * 64  # 空格为0

        self.board[28] = 1
        self.board[35] = 1
        self.board[27] = -1  # 白子为 -1
        self.board[36] = -1
        self.black = 2
        self.white = 2
        self.space = 60  # 空格数量
        self.frontier = [False] * 64  # 周围有棋子的空格，方便查找下一步棋

        tk = [18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45]

        for i in tk:
            self.frontier[i] = True

        self.side = 1  # 当前执棋方为黑方
        self.newPos = -1  # 最新下子的位置
        self.newRev = []  # 最新反转棋子的位置
        self.nextIndex = []  # 下一步可走棋的位置
        self.next = {}  # 下一步可走棋的反转棋子
        self.nextNum = 0  # 下一步可走棋的数目
        self.prevNum = 0  # 上一步可走棋的数目

        self.findLocation()

    def update(self):
        self.black = 0
        self.white = 0
        for i in range(64):

            if self.board[i] == 1:
                self.black += 1
            if self.board[i] == -1:
                self.white += 1

        self.space = 64 - self.black - self.white
        self.findFontier()
        self.findLocation()
        self.updateKey()

    def updateKey(self):
        self.key = zobrist.updateKey(self)

    def __getitem__(self, key):
        if key >= len(self.board):
            return 0
        return self.board[key]

    def __setitem__(self, key, value):
        self.board[key] = value

    def get_reverse(self, i, j, la, ta):
        lk = 0

        i = dire(i, j)

        while i != 64 and self.board[i] == -self.side:
            ta[la] = i
            la += 1
            lk += 1
            i = dire(i, j)

        if i == 64 or self.board[i] != self.side:  # 在边界或者最后一个不为己方棋子，则无法翻转

            la -= lk

        return la, ta

    def findFontier(self):  # 查找周围有棋子的空格
        for i in range(64):
            if self.board[i] == 0:
                isFont = False
                for j in range(8):
                    t = dire(i, j)
                    if t != 64 and self.board[t] != 0:
                        isFont = True
                        break
                self.frontier[i] = isFont
            else:
                self.frontier[i] = False

    def findLocation(self):  # 查找可走的棋子
        self.nextIndex = []  # 下一步可走棋的位置
        self.next = {}  # 下一步可走棋的反转棋子

        for fi in range(64):
            if not self.frontier[fi]:
                continue
            # print(fi)
            la, ta = 0, [0] * 30
            for j in range(8):
                la, ta = self.get_reverse(fi, j, la, ta)
                # print(la)
            if la > 0:
                # print(fi,'la:',la)
                # if la != len(ta):
                ta = ta[:la]
                self.next[fi] = ta
                self.nextIndex.append(fi)
        self.nextNum = len(self.nextIndex)
        return self.nextNum

    def pass_step(self):
        self.side = -self.side
        self.prevNum = self.nextNum
        self.key = zobrist.swap(self.key)

    def step(self, n):
        self.board[n] = self.side
        self.key = zobrist.set(self.key, 0 if self.side == 1 else 1, n)

        self.frontier[n] = False
        for i in range(8):
            k = dire(n, i)
            if k != 64 and self.board[k] == 0:
                self.frontier[k] = True
        reverses = self.next[n]
        re_len = len(reverses)
        for ri in reverses:
            self.board[ri] = self.side  # 反转的棋子
            self.key = zobrist.set(self.key, 2, ri)

        if self.side == 1:
            self.black = self.black + re_len + 1
            self.white = self.white - re_len
        else:
            self.white = self.white + re_len + 1
            self.black = self.black - re_len

        self.space = 64 - self.black - self.white
        self.side = -self.side
        self.key = zobrist.swap(self.key)
        self.prevNum = self.nextNum

    def is_finished(self):

        if self.space == 0:
            return True

        self.findLocation()

        if self.nextNum == 0:
            if self.prevNum == 0:
                return True
            self.pass_step()
            return self.is_finished()

        return False

    def get_winner(self):
        if self.black == self.white:
            return 0
        if self.black > self.white:
            return 1
        if self.black < self.white:
            return -1

    def show(self, show_frontier=False):
        print('黑子个数:{} 白子个数:{} 下一步可下位置个数:{}'.format(self.black, self.white, self.nextNum))
        for i in range(8):
            b = []
            for j in range(8):
                k = self.board[i * 8 + j]
                if k == 0:
                    if show_frontier and self.frontier[i * 8 + j]:
                        b.append('f')
                    else:
                        b.append('.')
                if k == 1:
                    b.append('b')
                if k == -1:
                    b.append('w')
            print(b)

        # if show_frontier:
        #     self.show_front()

    def show_front(self):
        for i in range(8):
            b = []
            for j in range(8):
                if self.frontier[i * 8 + j]:
                    b.append('f')
                else:
                    b.append('.')
            print(b)


def newMap(m, n):
    new_map = copy.deepcopy(m)
    new_map.step(n)

    return new_map


dr = [-8, -7, 1, 9, 8, 7, -1, -9]
bk = [8, 0, 0, 0, 8, 7, 7, 7]


def dire(i, d):  # 获取某一棋盘格某一方向的格子.超过边界返回64
    i += dr[d]
    return 64 if (i & 64) != 0 or (i & 7) == bk[d] else i
