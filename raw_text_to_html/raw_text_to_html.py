file = open("text.txt", "r", encoding='utf8')
content = file.readlines()
content = [x.strip() for x in content]
content = [x.strip('\u202c') for x in content]
content = [x.strip('\u202d') for x in content]


def addtag(ln, prefix, suffix, ind1, ind2):
    if len(ln) == 0 or (not ind1 in ln):
        return ln
    tmpln = ln
    ind = [-1,-1]
    for x in range(len(tmpln)):
        if tmpln[x] == ind1:
            ind[0] = x
        elif tmpln[x] == ind2:
            ind[1] = x
    if ind[1] == -1:
        ind[1] = len(tmpln)
    #print(ind1, ind)
    return addtag(tmpln[0:ind[0]], prefix, suffix, ind1, ind2) + prefix + tmpln[ind[0]:ind[1]+1] + suffix + tmpln[ind[1]+1:]


for i in range(len(content)):
    if len(content[i]) > 0:
        if '「' in content[i]:
            #print('「 found')
            content[i] = addtag(content[i], '<strong class="msg">', '</strong>', '「', '」')
        if ':' in content[i]:
            flag = True
            post = False
            tmp=[]
            for x in content[i]:
                tmp.append(x.isnumeric())
                if x == ':' and tmp[len(tmp)-2]==True:
                    post = True
            if post==True:
                content[i] = '<strong class="sage">' + content[i] + '</strong>'
        if '『' in content[i]:
            #print('『 found')
            content[i] = addtag(content[i], '<strong class="msg2">', '</strong>', '『', '』')
        if '【' in content[i]:
            content[i] = addtag(content[i], '<strong class="magic">', '</strong>', '【', '】')
        if '（' in content[i]:
            content[i] = addtag(content[i], '<strong class="think">', '</strong>', '（', '）')
        if '(' in content[i]:
            content[i] = addtag(content[i], '<strong class="think">', '</strong>', '(', ')')
        content[i] = '<p>' + content[i] + '</p>'
file.close()
outfile = open("content.txt", "w", encoding='utf8')
for i in content:
    outfile.write(i+'\n')
outfile.close()
