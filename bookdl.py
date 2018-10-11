import requests
from threading import Thread
import queue 
import re
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# global variable 
url = "https://bookdl.com/page/"
Q = queue.Queue()



if __name__ == "__main__":
    url = "https://bookdl.com"
    res = requests.get(url,verify=False)
    rs = re.findall(r'<h2.*?class=\"post-title\".*?href="(.*?)".*?rel=\"bookmark\".*?title=\"(.*?)\">.*?</a></h2>',res.text)
    print(res.text)
    for r in rs:
        print("{}:{}\n".format(r(1),r(0)))

