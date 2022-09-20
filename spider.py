#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Education Story and xiyouji get

import json
from fake_useragent import UserAgent
from  bs4 import BeautifulSoup
from collections import deque
import requests

class Spider(object):
    def __init__(self, log_dir="./") -> None:
        self.log_dir = log_dir
        self.failure = []
        self.init_rand_header()
        
    def init_rand_header(self):
        #ua = UserAgent(use_cache_server=False)
        ua = UserAgent()
        self.headers = {'User-Agent': ua.random}

    def init_wait_list(self, rooturl:str, urlfile:str):
        wait_list = deque()#FIFO queue
        # rewarite for root dir to generate waiting list 
        # or load a url list 
        raise NotImplementedError

    def bs4_parse(self,url,decode_style="GBK"):
        res = requests.get(url=url, headers=self.headers)

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

    def run(self):
        pass

