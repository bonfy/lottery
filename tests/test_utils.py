# -*- coding:utf-8 -*-

from lottery.utils import (str_to_lst, dct_add_dct, dct_add_lst_with_weight)


def test_str_to_lst():
    string = '1 2 10 12 14'
    lst = str_to_lst(string)
    assert type(lst) is list
    assert lst == [1, 2, 10, 12, 14]


def test_dct_add_dct():
    dct1 = {1: 2, 2: 4, 3: 2, 4: 2}
    dct2 = {1: 3, 2: 5}

    dct = dct_add_dct(dct1, dct2)
    assert type(dct) is dict
    assert dct == {1: 5, 2: 9, 3: 2, 4: 2}


def test_dct_add_lst_with_weight():
    dct1 = {1: 2, 2: 4, 3: 2, 4: 2}
    lst = [1, 2, 3]

    # case lst < dct1.keys()
    dct = dct_add_lst_with_weight(dct1, lst, 1)
    assert type(dct) is dict
    assert dct == {1: 3, 2: 5, 3: 3, 4: 2}

    # case: lst > dct1.keys()
    lst = [1, 2, 3, 5]
    assert type(dct) is dict
    assert dct == {1: 3, 2: 5, 3: 3, 4: 2}
