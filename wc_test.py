# -8- coding = utf-8 -*-
# @Time : 2023/10/10 15:48
# @File : wc_test.py
# @Software : PyCharm

import jieba,sqlite3
from wordcloud import WordCloud
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np


conn = sqlite3.connect('movie_2023_10_10_08_49_27.db')
cursor = conn.cursor()
sql = "select one_comment from movie250"
data = cursor.execute(sql)
print('data>>>',data)
text = ''
for item in data:
    # print('item>>>',type(item))
    text = text + item[0]
print(text)
cursor.close()
conn.close()

cut = jieba.cut(text)
# print(cut)
wordlist = []
for word in cut:
    # if '的' in word:
    #     continue
    # elif '。' in word:
    #     continue
    # elif '，' in word:
    #     continue
    if word == '的':
        continue
    elif word == '。':
        continue
    elif word == '，':
        continue
    elif word == '了':
        continue
    elif word == '是':
        continue
    elif word == '你':
        continue
    elif word == '我':
        continue
    else:
        wordlist.append(word)
print(len(wordlist))
string = ' '.join(wordlist)
print(string)

img = Image.open('women.jpg')
img_arr = np.array(img)
wc = WordCloud(background_color='white',mask=img_arr,font_path='simkai.ttf')
wc.generate_from_text(string)

fig = plt.figure()
plt.imshow(wc)
plt.axis('off')
plt.savefig('wcd2.jpg',dpi=300)
print('保存完毕')