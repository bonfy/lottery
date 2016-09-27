# -*- coding:utf-8 -*-

"""
base.py
~~~~~~~

所有彩票适配器的基类
"""

import random


class Base:
    """
    rLen: 红球总个数
    bLen: 蓝球总个数
    rNum: 开奖红球个数
    bNum: 开奖蓝球个数
    hisUrl: 历史信息页面
    hisNum: 历史信息开奖条数 30 50 100
    """
    rLen = 35
    bLen = 12
    rNum = 5
    bNum = 2
    hisUrl = None
    hisNum = 50

    @property
    def rLst(self):
        """
        红球数组
        """
        return list(range(1, self.rLen + 1))

    @property
    def bLst(self):
        """
        篮球数组
        """
        return list(range(1, self.bLen + 1))

    def create(self):
        """
        创建纯随机
        """
        return random.sample(self.rLst, self.rNum), random.sample(self.bLst, self.bNum)

    def create_with_wt(self):
        """
        权重随机(包括冷号 和 历史信息权重)
        """
        pass

    def create_with_lucky(self):
        """
        带幸运号权重随机
        """
        pass

    def prompt(self):
        opt = u'请输入你要生成的随机组数(纯随机 权重随机 带幸运号权重随机)\n如： 1 2 2'
        ipt = input(opt)
        try:
            lst = ipt.split(' ')
            if len(lst) != 3:
                print(u'输入个数错误，使用作者预定义组数1 2 2')
                return 1, 2, 2
            return int(lst[0]), int(lst[1]), int(lst[2])
        except Exception:
            print(u'输入错误，使用作者预定义组数1 2 2')
            return 1, 2, 2
