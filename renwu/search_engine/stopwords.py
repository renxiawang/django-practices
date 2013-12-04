# coding=utf-8

def del_stopwords(tokens):
    tokens_without_stops = []
    for tok in tokens:
        if tok not in stopwords:
            tokens_without_stops.append(tok)

    return tokens_without_stops

# load stopwords
f = open('chinese_stopwords_list.txt', 'r')
stopwords = []
for one in f.readlines():
    stopwords.append(one.strip().decode('utf-8'))