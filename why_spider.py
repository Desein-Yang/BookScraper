from spider import Spider
import json
from collections import deque
import re


class WhyBookSpider(Spider):
    def __init__(self, log_dir="./") -> None:
        super().__init__(log_dir)

    def init_wait_list(self, rooturl: str, urlfile=None):    
        wait_list = deque()
        prefix = "https://www.xxbing.cc/book/186/186424/"
        #"http://book.sbkk8.com/gudai/sidawenxuemingzhu/xiyoujibaihuawen/"
        bs4_res = self.bs4_parse(rooturl)
        mulu = bs4_res.find_all("li",class_="float-list")
        for li in mulu:
            link = prefix + li.find_all("a")["href"]
            wait_list.append(link)
        return wait_list

    def get_page(self,res):
        title = res.find("h1").text
        contents = []
        content_divs = res.find_all("div",id="page-content")
        for div in content_divs:
            content_ps = div.find_all("br")
            for ps in content_ps:
                contents.append(self.filter(ps.text))
        return {
            "title":title,
            "content": contents
        }

    def filter(self,text):
        # remove a to "" in text 
        if "<a>" in text:
            start = re.search(r"<a>",text).start()
            end = re.search(r"</a>",text).end()
            text = text[:start] + text[end:]
        
        # nbsp
        if '&nbsp' in text:
            text = re.sub("&nbsp","",text)
            
        # white space 
        text = re.sub(" ","",text)
        return text

    def run(self,rooturl,savefile):
        waitlist = self.init_wait_list(rooturl)
        idx = 0
        while waitlist:
            url = waitlist.popleft()
            res = self.bs4_parse(url,decode_style=GBK)
            output_each = self.get_page(res)
            output_each["idx"]=idx
            output_each["url"]=url
            idx += 1
            self.save_content(output_each,savefile)

        if self.failure:
            self.save_content({"failure":self.failure},savefile)


#rooturl = "http://book.sbkk8.com/gudai/sidawenxuemingzhu/xiyoujibaihuawen/"
#rooturl = "http://book.sbkk8.com/gudai/sidawenxuemingzhu/hongloumengbaihuawen/"
#rooturl = "http://book.sbkk8.com/gudai/sidawenxuemingzhu/shuihuchuanbaihuawen/"
#spider = BookSpider()
rooturl = "https://www.xxbing.cc/book/186/186424/index.html"
spider = WhyBookSpider()
spider.run(rooturl=rooturl,savefile="whys.json")