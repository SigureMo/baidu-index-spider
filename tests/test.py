with open('../input.csv','r') as f:
    keywords=[]
    for line in f:
        keywords.append(line.replace('\n','').split(','))
    print(keywords[1:])
