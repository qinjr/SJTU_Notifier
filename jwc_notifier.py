import bs4
from urllib.request import urlopen
import datetime
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
import schedule
import time


send_list = []

def handle_page(url):
    html = urlopen(url)
    bsObj = bs4.BeautifulSoup(html.read(), "html.parser")
    info_tag_list = bsObj.findAll("td", {"height":"20", "valign":"top", "width":"580"})
    for info_tag in info_tag_list:
        info = info_tag.a.get_text().replace('\n', '')
        link = "http://jwc.sjtu.edu.cn/web/sjtu/" + info_tag.a["href"]
        time = info_tag.next_sibling.get_text().strip().strip('[').strip(']').strip()
        time = datetime.datetime.strptime(time, "%Y-%m-%d")
        now = datetime.datetime.now()

        time_delta = 5
        if now.date() - time.date() < datetime.timedelta(time_delta):
            send_list.append((info, link, time))    

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))

def send_email():
    #Form msg string to send
    msg_str = ""
    for info in send_list:
        msg_str += info[0] + '\n' + info[1] + '\n\n'

    from_addr = ""#addr of sender
    password = ""#pwd of login a sending server
    to_addr = ""#addr of receiver
    smtp_server = ""#SMTP server

    msg = MIMEText(msg_str, "plain", "utf-8")
    msg['From'] = _format_addr('SJTU_NOTIFIER<%s>' % from_addr)
    msg['To'] = _format_addr('Dear QJR<%s>' % to_addr)
    msg['Subject'] = Header('JWC INFO UPDATES', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25) #server object
    server.set_debuglevel(1) #print log
    server.login(from_addr, password) #login
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def job():
    handle_page("http://jwc.sjtu.edu.cn/web/sjtu/198076.htm")
    send_email()
    print("send")

#set auto run time using schedule
schedule.every().day.at("00:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)