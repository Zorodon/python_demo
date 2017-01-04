# -*- coding: utf-8 -*-
import json

def readMovieJson():
    inFile = open("items.json")
    text = inFile.read()
    movie_dict = json.loads(text)
    for movie in movie_dict:
        rank = movie["rank"][0]
        title = movie["title"][0]
        link = movie["link"][0]
        star = movie["star"][0]
        rate = movie["rate"][0]
        if movie["quote"]:
            quote = movie["quote"][0]
        else:
            quote = "暂无".decode("utf-8")
        type = movie["type"][1].strip()

        print  "top".decode("utf-8") + rank + ".".decode("utf-8") + \
                title + " 评分".decode("utf-8") + star + \
                '('.decode("utf-8") + rate + ')'.decode("utf-8") + \
                "\n类型: ".decode("utf-8") + type + \
                "\n链接: ".decode("utf-8") + link + \
                "\n豆瓣评论: ".decode("utf-8") + quote + "\n"


readMovieJson()