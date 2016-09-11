# -*- coding:utf-8 -*-

"""
从网上获取历次开奖信息
"""
from pyquery import PyQuery as pq
from utils import requests_get, str_to_lst, dct_add_lst_with_weight


URL_HIS = "http://baidu.lecai.com/lottery/draw/list/1/?type=latest&num={num}"
URL_COLD = ("http://baidu.lecai.com/lottery/draw/sorts/ajax_get_stats.php"
            "?lottery_type=1&play_type=101")


def init_balls_with_wt(f_num, b_num, wt=0):
    """
    初始化balls dict
    """
    f_lst = list(range(1, f_num + 1))
    b_lst = list(range(1, b_num + 1))
    f_wt = [wt] * f_num
    b_wt = [wt] * b_num
    f_dct = dict(zip(f_lst, f_wt))
    b_dct = dict(zip(b_lst, b_wt))
    return f_dct, b_dct


def get_lottery_history_dct(num):
    r = requests_get(URL_HIS.format(num=num))
    assert r.status_code == 200
    d = pq(r.text)
    redballs = d("td .redBalls")
    blueballs = d("td .blueBalls")

    f_dct, b_dct = init_balls_with_wt(35, 12, wt=1)

    for item in redballs:
        f_dct = dct_add_lst_with_weight(f_dct,
                                        str_to_lst(pq(item).text().strip()), 1)

    for item in blueballs:
        b_dct = dct_add_lst_with_weight(b_dct,
                                        str_to_lst(pq(item).text().strip()), 1)
    return f_dct, b_dct


if __name__ == '__main__':
    f_dct, b_dct = get_lottery_history_dct(50)
    print(f_dct)
    print(b_dct)
