from spider import Spider
import json
from collections import deque



class BookSpider(Spider):
    def __init__(self, log_dir="./") -> None:
        super().__init__(log_dir)

    def init_wait_list(self, rooturl: str, urlfile=None):    
        wait_list = deque()
        prefix = "http://book.sbkk8.com"
        #"http://book.sbkk8.com/gudai/sidawenxuemingzhu/xiyoujibaihuawen/"
        bs4_res = self.bs4_parse(rooturl)
        mulu = bs4_res.find_all("li",class_="mululist")
        for li in mulu:
            link = prefix + li.find_all("a")["href"]
            wait_list.append(link)
        return wait_list

    def get_page(self,res):
        title = res.find("h1",class_="articleH11").text
        contents = []
        content_divs = res.find_all("div",id="content")
        for div in content_divs:
            content_ps = div.find_all("p")
            for ps in content_ps:
                contents.append(ps.text.strip("\r\n"))
        return {
            "title":title,
            "content": contents
        }

    def run(self,rooturl,savefile):
        waitlist = self.init_wait_list(rooturl)
        idx = 0
        while waitlist:
            url = waitlist.popleft()
            res = self.bs4_parse(url)
            output_each = self.get_page(res)
            output_each["idx"]=idx
            output_each["url"]=url
            idx += 1
            self.save_content(output_each,savefile)

        if self.failure:
            self.save_content({"failure":self.failure},savefile)

class SanguoSpider(Spider):
    def __init__(self, log_dir="./") -> None:
        super().__init__(log_dir)

    def init_wait_list(self, rooturl: str, urlfile=None):    
        wait_list = deque()
        bs4_res = self.bs4_parse(rooturl,decode_style="utf8")
        mulu = bs4_res.find_all("li",class_="mb10")
        for li in mulu:
            link = str(li.find_all("a")[0]).split("\"")[1]
            wait_list.append(link)
        return wait_list

    def get_page(self,res):
        title = res.find_all("h1",class_="fw")[0].text
        contents = []
        content_divs = res.find_all("div",class_="info-con")
        for div in content_divs:
            content_ps = div.find_all("p")
            for ps in content_ps:
                contents.append(ps.text.strip('\n'))
        return {
            "title":title,
            "content": contents
        }

    def run(self,rooturl,savefile):
        waitlist = self.init_wait_list(rooturl)
        idx = 0
        while waitlist:
            url = waitlist.popleft()
            res = self.bs4_parse(url,decode_style="utf8")
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
rooturl = "https://www.sanguoku.com/yanyi/baihuawen/"
spider = SanguoSpider()
spider.run(rooturl=rooturl,savefile="sanguo.json")