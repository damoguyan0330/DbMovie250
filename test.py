# -8- coding = utf-8 -*-
# @Time : 2023/10/14 11:13
# @File : test.py
# @Software : PyCharm

from fake_useragent import UserAgent


ua = UserAgent().chrome
ua1 = UserAgent().random
print(ua)
print(ua1)
