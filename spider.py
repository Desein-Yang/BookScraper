#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Education Story and xiyouji get

import json
from fake_useragent import UserAgent
from  bs4 import BeautifulSoup
from collections import deque
import requests

requests.adapters.DEAULT_RETRIES = 5 
class Spider(object):
    def __init__(self, log_dir="./") -> None:
        self.log_dir = log_dir
        self.failure = []
        self.init_rand_header()
        
    def init_rand_header(self):
        #ua = UserAgent(use_cache_server=False)
        self.ua = UserAgent()

    def init_wait_list(self, rooturl:str, urlfile:str):
        wait_list = deque()#FIFO queue
        # rewarite for root dir to generate waiting list 
        # or load a url list 
        raise NotImplementedError

    def bs4_parse(self,url,decode_style="GBK"):
        headers = {'User-Agent': self.ua.random}
        res = requests.get(url=url, headers=headers)

        if res.status_code == 200:
            try:
                result=res.content.decode(decode_style,"ignore")
            except:
                #reslut=res.content.decode("utf-8")
                # https://blog.csdn.net/wang7807564/article/details/78164855
                self.failure.append(url)
            bs4_res=BeautifulSoup(result,'html.parser')
        else:
            self.failure.append(url)
            raise requests.exceptions.ConnectionError
        # except requests.exceptions.ConnectionError:
        #     res.status_code = "Connection refused"  
        return bs4_res

    def get_content(self, url:str, tgtkeys:list):
        # rewrite for each website
        raise NotImplementedError

    def save_content(self, content, filename:str):
        save_file = self.log_dir + '/' + filename
        fout = open(save_file,"a+", encoding="utf-8")
        if type(content) is dict:
            json.dump(content,fout,ensure_ascii=False)
        else:
            json.dump({
                "content":content
            },fout,ensure_ascii=False)
        fout.write("\n")

    def run(self,rooturl):
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

    def sleep(self,n):
        import time
        time.sleep(n)

