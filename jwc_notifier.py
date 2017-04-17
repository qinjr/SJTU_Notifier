import bs4
from urllib.request import urlopen
import datetime

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
            print(time)
            send_list.append((info, link, time))    


handle_page("http://jwc.sjtu.edu.cn/web/sjtu/198076.htm")
print(send_list)