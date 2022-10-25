# BookScraper

This is a simplest system of web scraper, which encapsulate basic and general function in spider.py (e.g., html parse(bs4), save content(json), random user agent(USAgent)). The project have a clean logic and suitable for freshman. You NEED to cutomize some web-dependent functions (e.g., init_wait_list, get_content, run) to as example shows to crawl your page. 


## Usage:
```
python book_spider.py
```

## Features:

- Encapsulated Modules: Wrap basic module in spider.py (e.g., html parse(bs4), save content(json), random user agent(USAgent))
- Cutomized Modules: Customize function in subclass (e.g., init_wait_list, get_content, run)
- EXamples: Several examples to carwl datasets or book txt, or huggingface websites.
- Dataset/Rooturl: support load url list from file (dataset_spider.py) or parse from root url(book_spider.py)


## Requirement
```
requests                     2.26.0 
requests-oauthlib            1.3.1
beautifulsoup4               4.11.1
fake-useragent               0.1.11
```

## Contact

Please contact with me if any contribution or problem (yangqi@idea.edu.cn).
