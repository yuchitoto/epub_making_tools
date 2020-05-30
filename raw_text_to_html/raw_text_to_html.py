import csv


class PTagger:
    def __init__(self, rule):
        self.rule = rule
        #self.rule = rule.copy()


    def tag(self, content):
        #content = content.copy()
        rule = self.rule
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
                # normal rule handling
                for r in rule:
                    if r[0] in content[i]:
                        content[i] = addtag(content[i], r[2], r[3], r[0], r[1])
                # special cases
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

                # new paragraph tag for each lines
                content[i] = '<p>' + content[i] + '</p>'
        return content


if __name__=='__main__':
    file = open("text.txt", "r", encoding='utf8')
    content = file.readlines()
    file.close()
    content = [x.strip() for x in content]
    content = [x.strip('\u202c') for x in content]
    content = [x.strip('\u202d') for x in content]

    file = open("rule.csv", "r", encoding='utf8')
    csvfile = csv.reader(filter(lambda row: row[0]!='#', file))
    rule = [row for row in csvfile]
    file.close()

    tagger = PTagger(rule)
    content = tagger.tag(content)

    outfile = open("content.txt", "w", encoding='utf8')
    for i in content:
        outfile.write(i+'\n')
    outfile.close()
