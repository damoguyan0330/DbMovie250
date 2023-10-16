# -8- coding = utf-8 -*-
# @Time : 2023/10/7 9:50
# @File : dbMovie.py
# @Software : PyCharm

import requests,time,sqlite3,os
import fake_useragent,re
from lxml import etree


def UA():
    ua = fake_useragent.UserAgent().random
    # print(ua)
    headers = {'User-Agent':ua}
    # print(headers)
    return headers

def get_page():
    datalist = []
    for i in range(10):
        url = f'https://movie.douban.com/top250?start={i*25}&filter='
        print(url)
        text = requests.get(url=url,headers=UA()).text
        # with open('page.html','w',encoding='utf-8') as f:
        #     f.write(text)
        # print(text)
        time.sleep(0.2)
        tree = etree.HTML(text)
        li_list = tree.xpath('//*[@id="content"]/div/div[1]/ol/li')
        '//*[@id="content"]/div/div[1]/ol/li[1]'
        for li in li_list:
            data = []
            # print(li)
            # rated = li.xpath('./div/div[1]/em/text()')[0]
            # data.append(rated)
            detail_src = li.xpath('./div/div[1]/a/@href')[0]
            data.append(detail_src)
            img_src = li.xpath('./div/div[1]/a/img/@src')[0]
            # print(detail_src,img_src)
            data.append(img_src)
            c_movie_name = li.xpath('./div/div[2]/div[1]/a/span[1]/text()')[0].strip()
            data.append(c_movie_name)
            e_movie_name = li.xpath('./div/div[2]/div[1]/a/span[2]/text()')

            if len(e_movie_name) == 0:
                e_movie_name = ''
            else:
                e_movie_name = e_movie_name[0].strip()
                e_movie_name = re.sub('/\xa0', '', e_movie_name)
            data.append(e_movie_name)
            o_movie_name = li.xpath('./div/div[2]/div[1]/a/span[3]/text()')
            if len(o_movie_name) == 0:
                o_movie_name = ''
            else:
                o_movie_name = o_movie_name[0].strip()
                o_movie_name = re.sub('/\xa0','',o_movie_name)
            data.append(o_movie_name)
            # print(c_movie_name)
            # print(e_movie_name)
            # print(o_movie_name)
            da_name = li.xpath('./div/div[2]/div[2]/p[1]/text()[1]')[0].strip()
            da_name = re.sub('\xa0','',da_name)
            # print(da_name)
            data.append(da_name)
            movie_type = li.xpath('./div/div[2]/div[2]/p[1]/text()[2]')[0].strip()
            movie_type = re.sub('\xa0','',movie_type)
            # print(movie_type)
            data.append(movie_type)
            score = li.xpath('./div/div[2]/div[2]/div/span[2]/text()')[0]
            # print(score)
            data.append(score)
            comment_num = li.xpath('./div/div[2]/div[2]/div/span[4]/text()')[0].split('人')[0]
            # print(comment_num)
            data.append(comment_num)
            one_comment = li.xpath('./div/div[2]/div[2]/p[2]/span/text()')
            if len(one_comment) == 0:
                one_comment = ''
            else:
                one_comment = one_comment[0]
            # print(one_comment)
            data.append(one_comment)
            print(f'[{c_movie_name}]爬取完毕')
            # print(data)
            datalist.append(data)
        # break
    print(datalist)
    return datalist


def initDb():
    if os.path.exists(db_path):
        os.remove(db_path)

    sql = '''
    create table movie250(
    id integer primary key autoincrement,
    info_link text,
    pic_link text,
    cname varchar,
    ename varchar,
    oname varchar,
    da_name varchar,
    movie_type varchar,
    score numeric,
    comment_num numeric,
    one_comment text
    )
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def saveToDb():
    initDb()
    datalist = get_page()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    for data in datalist:
        for i in range(len(data)):
            if i == 7 or i == 8:
                continue
            else:
                data[i] = '"' + data[i] + '"'
        sql = '''insert into movie250(info_link,pic_link,cname,ename,oname,da_name,movie_type,score,comment_num,one_comment) values(%s)'''%','.join(data)
        # print(sql)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()




if __name__ == '__main__':
    # datalist = []
    # url = 'https://movie.douban.com/top250?start=0&filter='
    # get_page()

    t = time.strftime('%Y_%m_%d_%H_%M_%S')
    print(t)

    db_path = f'movie_{t}.db'
    print(db_path)



    # for i in range(10):
    #     url = f'https://movie.douban.com/top250?start={i*25}&filter='
    #     print(url)
    # get_page()
    saveToDb()


