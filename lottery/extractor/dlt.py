# -*- coding:utf-8 -*-

"""
DLT
"""

from pyquery import PyQuery as pq
from .base import Base
from ..utils import (create_lottery_number_with_weight,
                     create_lottery_number_with_lucky,
                     requests_get, init_balls_with_wt,
                     dct_add_lst_with_weight, str_to_lst,
                     dct_change_cold_weight, dct_add_dct)
from ..const import LuckyLst, LuckyWt


class DLT(Base):

    hisUrl = "http://baidu.lecai.com/lottery/draw/list/1/?type=latest&num={num}"
    coldUrl = ("http://baidu.lecai.com/lottery/draw/sorts/ajax_get_stats.php?lottery_type=1&play_type=101")

    def __init__(self):
        Base.__init__(self)
        self.init_dct()

    def init_dct(self):
        self.rDct, self.bDct = self._get_lottery_dct()

    def _get_lottery_dct(self):
        """
        返回中奖号码权重， 包括 往期开奖号码 及 冷号权重
        """
        r_dct, b_dct = self._get_lottery_history_dct(self.hisNum)
        c_red_dct, c_blue_dct = self._get_lottery_cold_dct()
        rDct = dct_add_dct(r_dct, c_red_dct)
        bDct = dct_add_dct(b_dct, c_blue_dct)
        return rDct, bDct

    def _get_lottery_history_dct(self, num, hisWt=1):
        """
        根据往期开奖结果 获得权重
        num:  历史期数 30 50 100
        hisWt:每出现一次，权重加几  默认为1
        """

        r_dct, b_dct = init_balls_with_wt(self.rLen, self.bLen, wt=1)
        r = requests_get(self.hisUrl.format(num=num))
        assert r.status_code == 200
        d = pq(r.text)
        redballs = d("td .redBalls")
        blueballs = d("td .blueBalls")

        for item in redballs:
            r_dct = dct_add_lst_with_weight(r_dct,
                                            str_to_lst(pq(item).text().strip()), hisWt)

        for item in blueballs:
            b_dct = dct_add_lst_with_weight(b_dct,
                                            str_to_lst(pq(item).text().strip()), hisWt)
        return r_dct, b_dct

    def _get_lottery_cold_dct(self, coldWt=10):
        """
        根据往期的冷号情况 返回冷号权重
        """
        r = requests_get(self.coldUrl)
        assert r.status_code == 200
        data = r.json()
        analyse_data = data.get('analysis_data', None)
        assert analyse_data
        items = analyse_data.get('cold_appear', None)
        assert len(items) == 2
        c_red_rst = dict((int(item["ball"]), int(item["nums"])) for item in items[0])
        c_blue_rst = dict((int(item["ball"]), int(item["nums"])) for item in items[1])
        # 冷号权重 = coldWt - 出现次数
        c_red_dct = dct_change_cold_weight(c_red_rst, wt=coldWt)
        c_blue_dct = dct_change_cold_weight(c_blue_rst, wt=coldWt)
        return c_red_dct, c_blue_dct

    def create_with_wt(self):
        if self.rDct and self.bDct:
            # dct copy, 防止调用修改原dct
            return create_lottery_number_with_weight(self.rDct.copy(), self.bDct.copy(), self.rNum, self.bNum)
        else:
            print("dict error")

    def create_with_lucky(self):
        if self.rDct and self.bDct:
            # dct copy, 防止调用修改原dct
            return create_lottery_number_with_lucky(self.rDct.copy(), self.bDct.copy(), self.rNum, self.bNum, LuckyLst, LuckyWt)
        else:
            print("dict error")

    def show(self):
        """
        展示
        """
        n, w, l = self.prompt()
        print(u'大乐透随机摇号：')
        print(u'-'*10)
        if n:
            print(u'纯随机')
            for i in range(n):
                print(self.create())

        if w:
            print(u'权重随机')
            for i in range(w):
                print(self.create_with_wt())

        if l:
            print(u'幸运数字')
            for i in range(l):
                print(self.create_with_lucky())

