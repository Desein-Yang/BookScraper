from spider import Spider
import json
from collections import deque


class SanguoRoleSpider(Spider):
    def __init__(self, log_dir="./") -> None:
        super().__init__(log_dir)

    def init_wait_list(self, rooturl: str, urlfile=None):    
        wait_list = deque()
        bs4_res = self.bs4_parse(rooturl,decode_style="utf8")
        mulu = bs4_res.find_all("dl",class_="news-item")
        for li in mulu:
            link = li.find("dd").find("a")["href"]
            wait_list.append(link)
        return wait_list

    def get_page(self,res):
        min_len = 100
        contents = []
        content_divs = res.find_all("div",class_="info-con")
        
        title = content_divs[0].find("img")["title"]
        for div in content_divs:
            content_ps = div.find_all("p")
            for ps in content_ps:
                if len(ps.text.strip('\n')) > min_len:
                    contents.append(ps.text.strip('\n'))
        return {
            "name":title,
            "content": contents
        }

    def run(self,rooturl,savefile,idx=0):
        waitlist = self.init_wait_list(rooturl)
        #idx = 0 global idx
        while waitlist:
            url = waitlist.popleft()
            res = self.bs4_parse(url,decode_style="utf8")
            output_each = self.get_page(res)
            if len(output_each["content"]) > 0:
                output_each["idx"]=idx
                output_each["url"]=url
                idx += 1
                self.save_content(output_each,savefile)
        self.sleep(3)

        if self.failure:
            self.save_content({"failure":self.failure},savefile)

        return idx


spider = SanguoRoleSpider()
savefile = "sanguo_role2.json"
# global idx
idx = 0

# ALL country
# for i in range(1,10):
#     rooturl = f"https://www.sanguoku.com/renwu/index{i}.html"
#     spider.run(rooturl=rooturl,savefile=savefile)

for cou in ["wei","shu","wu"]:
    for i in range(1,4):
        rooturl = f"https://www.sanguoku.com/renwu/{cou}/index{i}.html"
        idx = spider.run(rooturl=rooturl,savefile=savefile, idx=idx)
for cou in ["donghan","zhuhou","zaiye","huangjinjun","xijin","shaoshuminzu"]:
    for i in range(1,2):
        rooturl = f"https://www.sanguoku.com/renwu/{cou}/index{i}.html"
        idx = spider.run(rooturl=rooturl,savefile=savefile, idx=idx)


