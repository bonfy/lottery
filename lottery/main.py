# coding:utf-8

#:
#: Author BONFY<foreverbonfy@163.com>
#:

import random


#: 随机生成一组彩票号码
def create_lottery_number(f_lst, b_lst, f_num, b_num):
    #: f_lst: 前区所有号码
    #: b_lst: 后区所有号码
    #: f_num: 前区选择个数
    #: b_num: 后区选择个数
    f_rst = random.sample(f_lst, f_num)
    b_rst = random.sample(b_lst, b_num)
    return sorted(f_rst), sorted(b_rst)


#: 带权重生成一组彩票号码
def create_lottery_number_with_weight(f_dct, b_dct, f_num, b_num):
    f_rst = _create_some_number_with_weight(f_dct, f_num)
    b_rst = _create_some_number_with_weight(b_dct, b_num)
    return sorted(f_rst), sorted(b_rst)


#: 输入权重dict 返回一个数字
def _create_one_number_with_weight(dct):
    #: dct : type dict
    total = sum(dct.values())
    rad = random.randint(1, total)
    cur_total = 0
    for k, v in dct.items():
        cur_total += v
        if rad <= cur_total:
            return k, v


#: 输入权重dict 返回一组数字(num)个
def _create_some_number_with_weight(dct, num):
    #: dct : type dict
    #: num : type int
    rst = []
    while num > 0:
        rst_k, rst_v = _create_one_number_with_weight(dct)
        rst.append(rst_k)
        del dct[rst_k]
        num = num - 1
    return sorted(rst)


def main():

    #: 例子： 大乐透
    #: 规则：
    #: 前：35 选 5  后：12 选 2

    #: 前区 35个号 选5
    f_lst = list(range(1, 35))
    #: 后区 12个号 选2
    b_lst = list(range(1, 12))

    lottery_number = 5

    print("纯随机：")
    print('-' * 10)
    for i in range(lottery_number):
        f, b = create_lottery_number(f_lst, b_lst, 5, 2)
        print("前区: ", f, "\t后区: ", b)

    print('\n' * 2)
    print("权重随机:")
    print('-' * 10)

    f_weight_lst = [random.randint(1, 10) for i in range(1, 35)]
    f_weight_dct = dict(zip(f_lst, f_weight_lst))

    b_weight_lst = [random.randint(1, 10) for i in range(1, 12)]
    b_weight_dct = dict(zip(b_lst, b_weight_lst))

    for i in range(lottery_number):
        f, b = create_lottery_number_with_weight(
            f_weight_dct, b_weight_dct, 5, 2)
        print("前区: ", f, "\t后区: ", b)

if __name__ == '__main__':
    main()
