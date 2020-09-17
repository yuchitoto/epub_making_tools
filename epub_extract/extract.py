import zipfile
import re
from bs4 import BeautifulSoup


if __name__ == '__main__':
    print('Enter epub location:')
    filename = 'D:/eBooks/Novels/[白]Nostalgia World Online WEB 6_69.epub'
    print('Open epub {}\n'.format(filename))

    epub = zipfile.ZipFile(filename)
    filelist = []
    files = {}
    tmp = None
    cur = None
    pat = '[0-9]+_[0-9]+'

    for i in epub.namelist():
        if re.search(pat+'.xhtml', i):
            filelist.append(i)

    print(filelist)

    layer_delim = '_'
    for i in filelist:
        tmp = re.split(layer_delim, re.search(pat, i)[0])
        cur = files
        for j in tmp:
            if not j in cur:
                cur[j] = {}
            cur = cur[j]
        cur['data'] = epub.open(i).read()
    print(files['4'].keys())

    cnt = 1
    tmp = list(map(lambda x: int(x), files.keys()))
    for i in range(min(tmp), max(tmp)+1):
        cur = files[str(i)]
        tmp2 = list(map(lambda x: int(x), cur.keys()))
        print(max(tmp2))
        for j in range(min(tmp2), max(tmp2)+1):
            soup = BeautifulSoup(cur[str(j)]['data'].decode('utf8'), 'html.parser')
            with open('n8340dj_chi/n8340dj_'+str(cnt)+'.txt', 'wt', encoding='utf8') as out:
                print("{} {} {}".format(i, j, cnt))
                out.write(soup.find('div').get_text())
                out.close()
            cnt += 1
