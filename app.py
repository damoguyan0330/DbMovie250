from flask import Flask,render_template,request
import sqlite3
import os.path
from mypage import Pagination

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,'movie_2023_10_14_11_00_41.db')
app = Flask(__name__)
print('BASE_DIR>>>',BASE_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def home():
    return index()


@app.route('/movie')
def movie():
    datalist = []
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = 'select * from movie250'
    data = cursor.execute(sql)
    for item in data:
        # print('item>>>',item)
        datalist.append(item)
    # print(datalist)
    page_obj = Pagination(current_page=request.args.get("page", 1), all_count=len(datalist), per_page_num=25)
    index_list = datalist[page_obj.start:page_obj.end]
    html = page_obj.page_html()
    return render_template('movie.html',index_list=index_list,html=html)


@app.route('/score')
def score():
    score = []
    num = []
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    sql = 'select score,count(score) from movie250 group by score'
    data = cursor.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])
    return render_template('score.html',score=score,num=num)

@app.route('/word')
def wc():
    return render_template('word.html')

@app.route('/team')
def team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
