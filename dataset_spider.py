
from spider import Spider
import json
from collections import deque


class NaturalConvSpider(Spider):
    def __init__(self, log_dir="./", save_file=None) -> None:
        super().__init__(log_dir)
        self.save_file = save_file

    def init_wait_list(self, urlfile):
        # "/cognitive_comp/common_data/dialogue/NaturalConv/train_merge.json"
        wait_list = deque()
        f = open(urlfile, "r", encoding="utf-8")
        for line in f.readlines():
            dic = json.loads(line)
            wait_list.append(dic["url"])
        return wait_list
         
    def get_content(self, url: str, tgtkeys: list):
        output = {}
        for k in tgtkeys:
            output[k] = " "
        try:
            res = self.bs4_parse(url)
            # title
            try:
                if "163" in url:
                    title, post_content = self.get_163(res)
                elif "qq" in url:
                    title, post_content = self.get_qq(res)
                output["title"] = title.strip("\n")
                output["post_content"] = post_content.strip("\n")
            except:
                self.failure.append(url)
        except:
            self.failure.append(url)
        return output 

    def get_163(res):
        title = res.find_all("title")[0].text
        post_content = res.find_all("div",class_="post_body")[0].text
        return title, post_content

    def get_qq(res):   
        title = res.find_all("h1",class_="title")[0].text
        post_content = res.find_all("section",class_="article")[0].text
        return title, post_content 

    def run(self):
        wait_list = self.init_wait_list() # url waiting list
        done_url = 0
        while wait_list:
            todo_url = wait_list.popleft()
            output = self.get_content(todo_url,tgtkeys=["title","post_content"])
            self.save_content(output,self.log_dir + "/" +self.savefile)
            
            done_url += 1
            if done_url % 100 == 0:
                print(f"{done_url} url are done, {len(wait_list)} url are waiting...")

        self.save_content(self.failure,self.log_dir + "/failure.txt")
