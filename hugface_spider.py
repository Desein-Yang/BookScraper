#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Education Story and xiyouji get

import json
from fake_useragent import UserAgent
from  bs4 import BeautifulSoup
from collections import deque
import requests
from spider import Spider

requests.adapters.DEAULT_RETRIES = 5 
class HugFaceSpider(Spider):
    def __init__(self, log_dir="./") -> None:
        super().__init__(log_dir)

    def init_wait_list(self, rooturl:str):
        wait_list = deque()#FIFO queue
        prefix = "https://huggingface.co"
        bs4_res = self.bs4_parse(rooturl,decode_style="utf-8")
        
        mulu = bs4_res.find_all("article",class_="overview-card-wrapper")
        for li in mulu:
            link = prefix + li.find("a")["href"]                        
            wait_list.append(link)
        return wait_list
                                                                
    def get_content(self, res, url):
        name = '/'.join(url.split('/')[-2:])
        section_right = res.find_all("section")[1]
        datadiv = section_right.find_all("div",class_="justify-between")[0]
        data = datadiv.find("dd").text
        example = section_right.find_all("span",class_="block")[0].text
        
        return {
            "name":name,
            "download":data,
            "example":example
        }

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

    def run(self, rooturl, savefile):
        waitlist = self.init_wait_list(rooturl)
        idx = 0
        while waitlist:
            url = waitlist.popleft()
            res = self.bs4_parse(url,decode_style="utf-8")
            output_each = self.get_content(res, url)
            output_each["idx"]=idx
            output_each["url"]=url
            idx += 1
            self.save_content(output_each,savefile)

        if self.failure:
            self.save_content({"failure":self.failure},savefile)
        

hf = HugFaceSpider()
hf.run(rooturl='https://huggingface.co/models?sort=downloads&search=question-generation',savefile='./qgmodel.json')
