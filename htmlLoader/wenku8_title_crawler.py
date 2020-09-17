import requests as req
from bs4 import BeautifulSoup
import re
import csv
import sys
from wenku8_classes import wenku8
from bookDB import db
from multiprocessing import Pool

tag_finde = re.compile("<[^>]*>")
date_finde = re.compile("：".encode('gbk').decode('latin-1'))
finder = '文库不再提供该小说的在线阅读与下载服务'.encode('gbk')


def crawl(obj):
    cur = obj

    ret = None

    print("load wenku8 book id={}".format(cur))
    res = req.get("https://www.wenku8.net/book/{}.htm".format(cur), timeout=30)
    soup = BeautifulSoup(res.text, 'html.parser', multi_valued_attributes=None)
    title = soup.title.encode('latin-1')
    if "出现错误".encode('gbk') in title:
        #print("https://www.wenku8.net/book/{}.htm".format(cur))
        ret = False
        print("failed: {}".format(cur))
    else:
        print(title.decode('gbk'))
        tmp = list(map(lambda x: x.strip(" "), tag_finde.sub("", title.decode('gbk')).split("-")))
        flag = 'true'
        for i in soup.findAll('b'):
            cmper = str(i).encode('latin-1')
            if finder in cmper:
                flag = 'false'

        last_update = None
        if flag == 'true':
            last_update = date_finde.split(str(soup.findAll('td', {'width':'20%'})[3]))[1]
        entry = {'id':cur, 'book_name':tmp[0], 'author':tmp[1], 'publisher':tmp[2], 'available':flag, 'last_update':last_update}
        ret = entry

    return ret


if __name__ == "__main__":
    usedID = wenku8.containedID()
    flag = True
    cur = 1
    fail_lim = 0
    mode = 'find new'
    while flag:
        print("Largest id in DB: {}".format(usedID[-1]))
        print("Enter start id:")
        cur = int(input())
        print("Enter number of consecutive fails allowed:")
        fail_lim = int(input())
        print("Enter mode: (find new / update)")
        mode = input()
        fg = input("start id: {}   mode: {} (y/n): ".format(cur, mode))
        if fg.casefold().strip(" ") == 'y' and mode in ['find new', 'update']:
            flag = False
    new_entries = list()
    update_entries = list()
    failed = 0

    thread = 12

    """
    while failed < fail_lim:
        if mode == 'find new' and cur in usedID:
            cur += 1
            failed = 0
            continue

        print("load wenku8 book id={}".format(cur))
        res = req.get("https://www.wenku8.net/book/{}.htm".format(cur))
        soup = BeautifulSoup(res.text, 'html.parser', multi_valued_attributes=None)
        title = soup.title.encode('latin-1')
        if "出现错误".encode('gbk') in title:
            #print("https://www.wenku8.net/book/{}.htm".format(cur))
            failed += 1
            print('failed: {}'.format(cur))
        else:
            #print(title.decode('gbk'))
            tmp = list(map(lambda x: x.strip(" "), tag_finde.sub("", title.decode('gbk')).split("-")))
            flag = 'true'
            for i in soup.findAll('b'):
                cmper = str(i).encode('latin-1')
                if finder in cmper:
                    flag = 'false'

            last_update = None
            if flag == 'true':
                last_update = date_finde.split(str(soup.findAll('td', {'width':'20%'})[3]))[1]
            entry = {'id':cur, 'book_name':tmp[0], 'author':tmp[1], 'publisher':tmp[2], 'available':flag, 'last_update':last_update}

            if mode == 'update' and cur in usedID:
                update_entries.append(entry)
            else:
                new_entries.append(entry)

            failed = 0

        cur+=1
    """

    with Pool(processes=thread) as pool:
        if cur <= usedID[-1]:
            res_to_known = pool.map(crawl, range(cur, usedID[-1] + 1))
            for i in res_to_known:
                if i != False and i['id'] in usedID:
                    update_entries.append(i)
                elif i != False:
                    new_entries.append(i)

        cur = usedID[-1]+1
        while failed < fail_lim:
            new_res = pool.map(crawl, range(cur, cur+thread))
            cur = cur + fail_lim
            for i in new_res:
                if i == False:
                    failed += 1
                else:
                    new_entries.append(i)
                    failed = 0

    print(cur-1)
    #print(new_entries)

    with db.atomic():
        if len(new_entries) > 0:
            wenku8.insert_many(new_entries).execute()
        print("finished inserting new entries")

        if mode == 'update' and len(update_entries) > 0:
            for i in update_entries:
                wenku8.update(i).where(wenku8.id==i['id']).execute()
            print("finished updating entries")

    print("program terminates")
