import requests
import json
import pymysql
from multiprocessing.dummy import Pool as ThreadPool
import time

def getsource(url):
    post_data = {
        'mid':url.replace('https://space.bilibili.com/', ''),
        'csrf': 'null'
    }
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    headers = {
        'Host': 'space.bilibili.com',
        'Referer': 'https://space.bilibili.com/' + str(i),
        'Origin': 'https://space.bilibili.com',
        'User-Agent': agent,
        'X-Requested-With': 'XMLHttpRequest'
    }

    json_content = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo',headers=headers,data=post_data).json()
    if json_content['status'] == True:
        if 'data' in json_content:
            json_data = json_content['data']
            mid = json_data['mid']
            name = json_data['name']
            sex = json_data['sex']
            face = json_data['face']
            description = json_data['description']
            level = json_data['level_info']['current_level']
            birthday = json_data['birthday'] if 'birthday' in json_data.keys() else 'nobirthday'
            place = json_data['place'] if 'place' in json_data.keys() else 'noplace'

            try:
                res = requests.get(
                    'https://api.bilibili.com/x/space/navnum?mid=' + str(mid) + '&jsonp=jsonp').text
                js_fans_data = json.loads(res)
                following = js_fans_data['data']['following']
                fans = js_fans_data['data']['follower']
            except:
                following = 0
                fans = 0
        else:
            print('no data')

        try:
            conn = pymysql.connect(host='localhost',user='root',passwd='123456',db='bilibiliDB',charset='utf8')
            cur = conn.cursor()
            cur.execute('INSERT INTO bilibili_user_info(mid,name,sex,face,birthday,place,description, \
            following,fans,level) \
            VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' \
            % (mid,name,sex,face,birthday,place,description,following,fans,level))
            conn.commit()
            print('get bilibili ' + str(i) + '\n')
        except Exception:
            print('MySQL Error')
    else:
        print('post fail')

if __name__ == '__main__':
    urls = []
    for i in range(1, 2):
        url = 'https://space.bilibili.com/' + str(i)
        urls.append(url)
    pool = ThreadPool()
    results = pool.map(getsource,urls)
    pool.close()
    pool.join()

