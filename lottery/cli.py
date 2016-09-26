# -*- coding:utf-8 -*-

"""

Lottery
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Author BONFY<foreverbonfy@163.com>
"""

import random
from balls import get_lottery_history_dct
from utils import create_lottery_number_with_weight


def create_lottery_number(f_lst, b_lst, f_num, b_num):
    """
    随机生成一组彩票号码
    param: f_lst: 前区所有号码
    param: b_lst: 后区所有号码
    param: f_num: 前区选择个数
    param: b_num: 后区选择个数
    """
    f_rst = random.sample(f_lst, f_num)
    b_rst = random.sample(b_lst, b_num)
    return sorted(f_rst), sorted(b_rst)


def main():
    # 1组纯随机
    num_lottery = 1
    f_lst = list(range(1, 35))
    b_lst = list(range(1, 12))
    print("纯随机：")
    print('-' * 10)
    for i in range(num_lottery):
        f, b = create_lottery_number(f_lst, b_lst, 5, 2)
        print("前区: ", f, "\t后区: ", b)

    # 2组权重随机
    num_lottery = 2
    f_his_dct, b_his_dct = get_lottery_history_dct(50)

    print('\n' * 2)
    print("权重随机:")
    print('-' * 10)

    for i in range(num_lottery):
        f, b = create_lottery_number_with_weight(
            f_his_dct.copy(), b_his_dct.copy(), 5, 2)
        print("前区: ", f, "\t后区: ", b)


if __name__ == '__main__':
    main()
