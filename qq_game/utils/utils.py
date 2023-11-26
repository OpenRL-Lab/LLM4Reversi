import random


def rnd():  # 获取32位的随机数
    return int(random.random() * 0x100000000)
