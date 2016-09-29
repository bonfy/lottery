# -*- coding:utf-8 -*-


import requests
from requests.exceptions import ConnectionError, Timeout
import random
import urllib

##################
#
#  requests 封装
#
##################


def requests_get(url, **kwargs):

    PROXIES = None

    # 如果有代理，请把下面注释去掉
    # 自行处理

    # _usr = 'user'
    # _pwd = 'pwd'
    # _encoded_pwd = urllib.parse.quote(_pwd)

    # PROXIES = {
    #     'http': 'http://{usr}:{pwd}@proxy:port'.format(usr=_usr, pwd=_encoded_pwd),
    # }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/38.0.2125.122 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    try:
        r = requests.get(
            url,
            headers=HEADERS,
            proxies=PROXIES,
            **kwargs
        )
    except ConnectionError:
        print('Network connection failed.')
    except Timeout:
        print('timeout.')
    return r


##################
#
#  dict操作
#
##################

def str_to_lst(balls):
    """
    "1 4 5 6 8" -> [1,4,5,6,8]
    """
    assert isinstance(balls, str)
    return [int(i) for i in balls.split(' ')]


def dct_add_dct(x, y):
    """
    输入两个dict , 返回并集
    @return type: dict
    """
    from collections import Counter
    X, Y = Counter(x), Counter(y)
    rst = dict(X + Y)
    return rst


def dct_add_lst_with_weight(dct, lst, wt):
    """
    @param lst: 数字list
    @param wt : 权重
    @return type: dict

    """
    # 万一设置幸运数字 所有可选号之中
    # 例如 双色球没有35

    # 本来想用在幸运数字中的，发现没有用到
    # 反而用在了 历史号的权重上了
    # AnyWay 保险点，多加个判断总是没错的

    rs = set(lst) - set(dct.keys())
    if rs:
        for i in list(rs):
            lst.remove(i)
    wt = [wt] * len(lst)
    dct_wt = dict(zip(lst, wt))
    rst = dct_add_dct(dct, dct_wt)
    return rst


def dct_change_cold_weight(dct, wt=10):
    """
    改变冷号的权重
    如果最近30期 数字只出现1次 权重就为 wt-1
    """
    for key in dct:
        dct[key] = wt - dct[key] if wt > dct[key] else 0
    return dct

##################
#
#   初始化
#
##################


def init_balls_with_wt(r_len, b_len, wt=0):
    """
    初始化balls dict
    """
    r_lst = list(range(1, r_len + 1))
    b_lst = list(range(1, b_len + 1))
    r_wt = [wt] * r_len
    b_wt = [wt] * b_len
    r_dct = dict(zip(r_lst, r_wt))
    b_dct = dict(zip(b_lst, b_wt))
    return r_dct, b_dct

##################
#
#  随机操作
#
##################


def create_lottery_number_with_weight(f_dct, b_dct, f_num, b_num):
    """
    带权重生成一组彩票号码
    """
    f_rst = create_some_number_with_weight(f_dct, f_num)
    b_rst = create_some_number_with_weight(b_dct, b_num)
    return sorted(f_rst), sorted(b_rst)


def create_lottery_number_with_lucky(f_dct, b_dct, f_num, b_num, lucky_lst, lucky_wt):
    f_rst = create_number_weight_luckynumber(f_dct, lucky_lst, lucky_wt, f_num)
    b_rst = create_number_weight_luckynumber(b_dct, lucky_lst, lucky_wt, b_num)
    return sorted(f_rst), sorted(b_rst)


def create_one_number_with_weight(dct):
    """
    输入权重dict 返回一个数字
    """
    total = sum(dct.values())
    # 将keys乱序，使结果更加随机
    # print(type(dct.keys()))
    keys_lst = list(dct.keys())
    random.shuffle(keys_lst)

    rad = random.randint(1, total)
    cur_total = 0
    for k in keys_lst:
        cur_total += dct[k]
        if rad <= cur_total:
            return k


def create_some_number_with_weight(dct, num):
    """
    输入权重dict 返回一组数字(num)个
    """
    rst = []
    while num > 0:
        rst_k = create_one_number_with_weight(dct)
        rst.append(rst_k)
        del dct[rst_k]
        num = num - 1
    return sorted(rst)


def create_number_weight_luckynumber(dct,
                                     lucky_lst,
                                     lucky_weight,
                                     num):
    """
    输入权重dict 和 幸运数字 返回一组数字(num)个
    """
    for item in lucky_lst:
        if item in dct:
            # print(item, ' in dict')
            dct[item] += lucky_weight
    return create_some_number_with_weight(dct, num)


def lottery_number_to_pt(tup):
    rLst, bLst = tup
    r = ' '.join([num_to_str(i) for i in rLst])
    b = ' '.join([num_to_str(i) for i in bLst])
    return r + '  ' + b


def num_to_str(num):
    if num < 10:
        return '0'+str(num)
    else:
        return str(num)
