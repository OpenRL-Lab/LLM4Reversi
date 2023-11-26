from utils.utils import rnd


class Zobrist:
    def __init__(self):
        self.swapSide = [rnd(), rnd()]  # 下棋方轮换的附加散列码
        self.zarr = [[[] for _ in range(64)], [[] for _ in range(64)], [[] for _ in range(64)]]
        for pn in range(64):
            self.zarr[0][pn] += [rnd(), rnd()]  # 各位置上出现黑棋时
            self.zarr[1][pn] += [rnd(), rnd()]  # 各位置上出现白棋时
            self.zarr[2][pn] += [self.zarr[0][pn][0] ^ self.zarr[1][pn][0],
                                 self.zarr[0][pn][1] ^ self.zarr[1][pn][1]]  # 各位置上翻棋时

    def updateKey(self, map):
        key = [0, 0]
        for i in range(64):
            if (map[i] == 1):
                key[0] ^= self.zarr[0][i][0]
                key[1] ^= self.zarr[0][i][1]
            if (map[i] == -1):
                key[0] ^= self.zarr[1][i][0]
                key[1] ^= self.zarr[1][i][1]
        key[0] ^= self.swapSide[0]
        key[1] ^= self.swapSide[1]
        if map.side == -1:
            key[0] ^= self.swapSide[0]
            key[1] ^= self.swapSide[1]
        return key

    def swap(self, key):  # 执棋方轮换
        key[0] ^= self.swapSide[0]
        key[1] ^= self.swapSide[1]
        return key

    def set(self, key, pc, pn):  # 设置更新key
        key[0] ^= self.zarr[pc][pn][0]
        key[1] ^= self.zarr[pc][pn][1]
        return key


class HashNode:
    def __init__(self):
        self.key = None
        self.eva = 0
        self.depth = -10
        self.flags = None
        self.best = None


class HashTable:
    def __init__(self):
        self.HASH_SIZE = (1 << 19) - 1  # 存储单元数为 524287
        self.data = {}

    def set(self, key, eva, depth, flags, best):
        keyb = key[0] & self.HASH_SIZE

        if not keyb in self.data:
            self.data[keyb] = HashNode()

        if self.data[keyb].key == key[1] and self.data[keyb].depth > depth:
            # 局面相同 并且 记录比当前更深 则不替换
            return

        self.data[keyb].key = key[1]
        self.data[keyb].eva = eva
        self.data[keyb].depth = depth
        self.data[keyb].flags = flags
        self.data[keyb].best = best

    def get(self, key, depth, alpha, beta):
        keyb = key[0] & self.HASH_SIZE
        if not keyb in self.data:
            return None

        phashe = self.data[keyb]
        if phashe.key != key[1] or phashe.depth < depth:
            return None

        if phashe.flags == 0:
            return phashe.eva
        elif phashe.flags == 1:
            if phashe.eva <= alpha:
                return phashe.eva
            return None
        elif phashe.flags == 2:
            if phashe.eva >= beta:
                return phashe.eva
            return None
        else:
            print('data flags is wrong!')
            return None

    def getBest(self, key):
        keyb = key[0] & self.HASH_SIZE
        if not keyb in self.data:
            return None

        phashe = self.data[keyb]
        if phashe.key != key[1]:
            return None
        return phashe.best
