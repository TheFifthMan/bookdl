import requests
from threading import Thread
from bs4 import BeautifulSoup
import queue 
import re
import threading 
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
from datetime import datetime 
now = datetime.now()
timestamp = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)+str(now.second)

# global variable 
# url = "https://bookdl.com/page/"
Q = queue.Queue()

session = requests.Session()
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}
last_page_pattern = '#page > div > div > div > div > div > nav > div > a.last'

def get_pages(cssselector):
    url = "https://bookdl.com"
    res = session.get(url,headers=headers)
    soup = BeautifulSoup(res.text,"html.parser")
    last_page = soup.select(cssselector)
    last = re.search(r'https://bookdl.com/page/(\d+)/',last_page[0].get('href'))
    return last.group(1) 

def request_all_links():
    for num in range(1,int(last)):        
        url = "https://bookdl.com/page/"+str(num)
        print('正在收集每一页的url:{}'.format(url))
        res = session.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        posts = soup.find_all('h2','post-title')
        for post in posts:
            a = post.find('a')
            title = a['title']
            link = a['href']
            Q.put(link)
            
   

def request_download_url():
    while not Q.empty():
        url = Q.get()
        print('下载链接：{} - {}'.format(url,datetime.now()))
        res = session.get(url,headers=headers)
        sourp = BeautifulSoup(res.text,'html.parser')
        div = sourp.find('div',class_='book-download')
        links = div.find_all('a')
        for link in links:
            print(link['href'])
            with open(timestamp+'.txt','a')as f:
                f.write(link['href']+'\n')
    
if __name__ == "__main__":
    last = get_pages(last_page_pattern)
    download = request_all_links()
    # request_download_url(download)
    ts = [threading.Thread(target=request_download_url) for i in range(100)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()

