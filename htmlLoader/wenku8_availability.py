#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as req
from bs4 import BeautifulSoup
import peewee
from peewee import *
from wenku8_classes import wenku8
from multiprocessing import Pool


def wenku8_get(id):
    return req.get("https://www.wenku8.net/book/{}.htm".format(id))


def availability_check(id):
    res = wenku8_get(id)
    soup = BeautifulSoup(res.text, 'html.parser', multi_valued_attributes=None)
    for i in soup.findAll('b'):
        cmper = i.encode('latin-1')
        finder = '文库不再提供该小说的在线阅读与下载服务'.encode('gbk')
        """
        print(i)
        print(cmper)
        print(finder)
        print()
        """
        if finder in cmper:
            return {'id':id, 'available':'false'}
    return {'id':id, 'available':'true'}


if __name__ == '__main__':
    with Pool(processes=4) as pooh:
        ids = wenku8.containedID()
        print(ids)

        availability = pooh.map(availability_check, ids)
        print("fetch page finished")

        truer = []
        falser = []
        for i in availability:
            if i['available'] == 'true':
                truer.append(i['id'])
            elif i['available'] == 'false':
                falser.append(i['id'])
            else:
                print('unknown reaction: {}'.format(i['id']))
        true_update = wenku8.update(available='true').where(wenku8.id << truer)
        true_update.execute()
        false_update = wenku8.update(available='false').where(wenku8.id << falser)
        false_update.execute()

        print('Update finished')
