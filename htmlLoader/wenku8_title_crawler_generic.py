import requests as req
from bs4 import BeautifulSoup
import re
import csv, json
import sys, getopt
from multiprocessing import Pool
import multiprocessing

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
        flag = True
        for i in soup.findAll('b'):
            cmper = str(i).encode('latin-1')
            if finder in cmper:
                flag = False

        last_update = None
        if flag == True:
            last_update = date_finde.split(str(soup.findAll('td', {'width':'20%'})[3]))[1]
        print('-'.join(tmp[0:-3]) + 'end')
        entry = {'id':cur, 'book_name':'-'.join(tmp[0:-3]), 'author':tmp[-3], 'publisher':tmp[-2], 'available':flag, 'last_update':last_update}
        ret = entry

    return ret


if __name__ == "__main__":
    thread = multiprocessing.cpu_count()

    arg, val = getopt.getopt(sys.argv[1:], "t:o:", ["threads=", "outformat="])

    out = 'csv'

    for ca, cv in arg:
        if ca in ("-t", "--threads"):
            thread = int(cv)
            print("Using {} threads".format(cv))
        elif ca in ('-o', '--outformat'):
            out = cv

    flag = True
    cur = 1
    fail_lim = 0
    while flag:
        print("Enter start id:")
        cur = int(input())
        print("Enter number of consecutive fails allowed:")
        fail_lim = int(input())
        fg = input("start id: {} (y/n): ".format(cur))
        if fg.casefold().strip(" ") == 'y':
            flag = False
    new_entries = list()
    failed = 0

    with Pool(processes=thread) as pool:
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

    if out == 'csv':
        with open('wenku8_index.csv', 'wt', encoding='utf8', newline='') as file:
            wrt = csv.DictWriter(file, fieldnames=list(new_entries[0].keys()))
            wrt.writeheader()
            wrt.writerows(new_entries)
    elif out == 'json':
        with open('wenku8_index.json', 'wt', encoding='utf8') as file:
            json.dump(new_entries, file)

    print("program terminates")
