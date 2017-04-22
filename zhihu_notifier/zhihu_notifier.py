import bs4
from urllib.request import urlopen
import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import schedule
import time
from zhihu import ZhihuClient

#people that I need to watch
author_list = ["ji-xuan-yi-9"]

#answer amount
answer_nums = []

def login():
    Cookies_File = 'cookies.json'
    client = ZhihuClient(Cookies_File)
    return client

def init_author_list(client):
    for i in range(len(author_list)):
        author_url = "https://www.zhihu.com/people/" + author_list[i]
        author_list[i] = client.author(author_url)

def init_answer_nums(client):
    for author in author_list:
        answer_nums.append(get_answer_num(author))

def get_answer_num(author):
    return author.answer_num

def get_answers(author, ans_need):
    answers = author.answers
    for i in range(ans_need):
        answers[i].save(filepath=author.name)

def job():
    for i in range(len(author_list)):
        new_ans_num = get_answer_num(author_list[i])
        if (new_ans_num > answer_nums[i]):
            author = author_list[i]
            ans_need = new_ans_num - answer_nums[i]
            get_answers(author, 4)
            answer_nums[i] = new_ans_num

##login and init
client = login()
init_author_list(client)
init_answer_nums(client)
print(author_list)
print(answer_nums)
job()

#set auto run
#schedule.every().day.at("00:00").do(job)
#while True:
 #   schedule.run_pending()
  #  time.sleep(1)
