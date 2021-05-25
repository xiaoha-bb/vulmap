
from pyquery import PyQuery as pq
import requests
from celery.utils.log import get_task_logger
from multiprocessing.dummy import Pool as ThreadPool
logger = get_task_logger(__name__)
from whois.parser import WhoisEntry,datetime_parse
import re
import json
import util
import whois


headers = {"User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)"}

'''
"creation_date": "2003-04-21 03:50:05",
"emails": "DomainAbuse@service.aliyun.com",
"expiration_date": "2021-04-21 03:50:05",
"registrar": "Alibaba Cloud Computing (Beijing) Co., Ltd."

'''

# def _extract_whois_info(domain):
#     try:
#         url = "https://ip.sb/whois/{}".format(domain)
#         text = requests.get(url,timeout=10).text
#         data = re.findall(r"<pre>(.+)</pre>", text, re.S)
#         _result = {}
#         if data:
#             if "Domain Name:" in data[0]:
#                 result = WhoisEntry.load(domain, data[0])
#             else:
#                 _result['msg'] = data
#                 return _result
#         else:
#             return ''
#         if result.get("domain_name"):
#             _result['creation_date'] = result.get("creation_date",'')
#             _result['emails'] = result.get("emails",'')
#             _result['expiration_date'] = result.get("expiration_date",'')
#             _result['registrar'] = result.get("registrar",'')
#         return _result
#     except Exception as e:
#         logger.warn(e)
#         return ''

def _extract_whois_info_by_whois(domain):
    try:
        result = whois.whois(domain)
        if not result:
            return ''
        _result = {}
        if result.get("domain_name"):
            _result['creation_date'] = result.get("creation_date",'')
            _result['emails'] = result.get("emails",'')
            _result['expiration_date'] = result.get("expiration_date",'')
            _result['registrar'] = result.get("registrar",'')
        return _result
    except Exception as e:
        logger.warn(e)
        return ''


def batch_extract_whois_info(doamins):
    arg_list = []
    pool = ThreadPool(5)
    def _run_process(args):
        result = {'domain':args,
                  'info':''}
        whois_info = _extract_whois_info_by_whois(args)
        if whois_info:
            result['info'] = whois_info
        util.save_whois_info(result)  # 保存数据
    for _domain in doamins:
        arg_list.append(_domain)
    pool.map(_run_process, arg_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    import sys
    import os
    logger.warn = print
    logger.info = print
    domains = []
    if len(sys.argv) != 2:
        print("python3 whois_scraper.py [TARGET-FILE]")
        sys.exit()
    target_file = sys.argv[1]
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            domains = f.readlines()
            domains = [i.strip() for i in domains]
        batch_extract_whois_info(domains) # 批量爬虫
    else:
        print("target file not found")
    # with open("7wdomain.txt", "r") as f:
    #     #domains = json.load(f)
    #     domains = f.readlines()
    #     domains = [i.strip() for i in domains]
    # batch_extract_whois_info(domains)

