import pymysql

def createDB():
    db = pymysql.connect(host='localhost', user='root', passwd='123456',db='bilibiliDB')
    cur = db.cursor()
    # cur.execute('create database if not exists bilibiliDB;')
    cur.execute('create table if not exists comment_info(id int not null auto_increment,userId varchar(11),nickname varchar(64),avatarUrl varchar(256),createTime varchar(20),likedCount varchar(11),content Text,primary key (id))')
    cur.close()
    db.commit()
    db.close()

if __name__ == '__main__':
    createDB()