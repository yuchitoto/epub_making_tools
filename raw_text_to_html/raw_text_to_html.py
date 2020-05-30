"""
Small tool to add p tag to each line in txt
This also tags suitable tags according to rules.csv which acts as css tag patterns
Version: 1.0.1
"""

import csv
from pTagger import PTagger

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
