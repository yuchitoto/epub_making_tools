"""
Small tool to add p tag to each line in txt
This also tags suitable tags according to rules.csv which acts as css tag patterns
Version: 1.0.1-formal
"""

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
                """if ':' in content[i]:
                    flag = True
                    post = False
                    tmp=[]
                    for x in content[i]:
                        tmp.append(x.isnumeric())
                        if x == ':' and tmp[len(tmp)-2]==True:
                            post = True
                    if post==True:
                        content[i] = '<strong class="sage">' + content[i] + '</strong>'"""

                # new paragraph tag for each lines
                content[i] = '<p>' + content[i] + '</p>'
        return content
