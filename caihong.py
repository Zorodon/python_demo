import requests
import json
import time
import pymysql

headers = {
    'Host':'music.163.com',
    'Referer':'http://music.163.com/song?id=185809',
    'Origin':'http://music.163.com',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0.3 Safari/604.5.6'
}
proxies = {
'http:': 'http://121.232.146.184',
'https:': 'https://144.255.48.197'
}
def get_json(url,page):
    params = {'limit':'20','offset':str((page-1)*20)}
    json_content = requests.get(url,params=params,headers=headers).content
    return json_content

def get_all_comments(url):

    json_text = get_json(url,1)
    json_dic = json.loads(json_text)
    comments_num = int(json_dic['total'])

    if(comments_num %20 == 0):
        page = int(comments_num/20)
    else:
        page = int(comments_num/20)+1

    print("彩虹一共有{0}条评论，一共{1}页".format(comments_num,page))

    for i in range(page):

        print("第{0}页...".format(i))
        json_text = get_json(url,i+1)
        json_dic = json.loads(json_text)

        for item in json_dic['comments']:
            userid = item['user']['userId']
            nickname = item['user']['nickname']
            avatarUrl = item['user']['avatarUrl']
            likedCount = item['likedCount']
            content = item['content']
            stamp = item['time']
            stamp = int(stamp*(10 ** (10-len(str(stamp)))))
            time_arr = time.localtime(stamp)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S',time_arr)

            # try:
            #     conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='caihongDB', charset='utf8mb4')
            #     cur = conn.cursor()
            #     cur.execute('INSERT INTO caihong_comment_table(userId,nickname,avatarUrl,createTime,likedCount,content) \
            #           VALUES("%s","%s","%s","%s","%s","%s")' \
            #                 % (userid, nickname, avatarUrl, time_str, likedCount, pymysql.escape_string(content)))
            #     conn.commit()
            # except pymysql.Error:
            #     print('MySQL Error')


if __name__ == '__main__':
    url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_185809'
    get_all_comments(url)


# create table if not exists comment_info(id int not null auto_increment,userId varchar(11),nickname varchar(64),avatarUrl varchar(256),createTime varchar(20),likedCount varchar(11),content Text,primary key (id))