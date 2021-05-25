from pyquery import PyQuery as pq
import requests
from celery.utils.log import get_task_logger
from multiprocessing.dummy import Pool as ThreadPool
from pymongo import MongoClient
import json
import util
import time

logger = get_task_logger(__name__)

headers = {"User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)",
           "Content-Type": "application/x-www-form-urlencoded",
           "Cookies":"bbsmax_user=4d320e5b-7575-41f5-b515-303c3058ff77;"} #

seos_headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Cookie": "PHPSESSID=l5hr65ee5vrn5q7otqvsvckedm; UM_distinctid=16e362ba574642-0e9041a95709f-1d3e6a5a-13c680-16e362ba5757d8; CNZZDATA1277700026=1874234083-1572865066-https%253A%252F%252Fwww.google.com%252F%7C1572865066"
}

mobile_cnzz_headers = {
    "Cookie": "CNZZDATA5082706=cnzz_eid%3D1392311694-1572918300-http%253A%252F%252Fmtool.chinaz.com%252F%26ntime%3D1572918300; UM_distinctid=16e396156d12d-0891a0842087f9-34505f20-5a900-16e396156d2130",
    "Content-Type": "application/x-www-form-urlencoded"
}

proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}

def _extract_filing_info(domains):
    try:
        result = []
        base_url = "http://icp.chinaz.com/searchs"
        _url = base_url
        if len(domains) == 0:
            logger.warn("not domain return!")
        _host = 'urls='
        for _domain in domains:
            _result = {}
            _result['domain'] = _domain
            _result['info'] = {'CompanyName':'',
                    'CompanyType':'',
                    'MainPage':'',
                    'SiteLicense':'',
                    'SiteName':'',
                    'VerifyTime':'',
                    }
            result.append(_result)
            _host += "{}%0D%0A".format(_domain)
        resp = requests.post(_url,data= _host,headers=headers)
        d = pq(resp.content)
        _info_list = d('tbody#result_table tr').items()
        for _info in _info_list:
            i = pq(_info)
            domain = i('td:nth-child(1)').text().strip()
            for _r in result:
                if _r['domain'] == domain:
                    _r['info']['CompanyName'] = i('td:nth-child(2)').text().strip()  # 主办单位
                    _r['info']['CompanyType'] = i('td:nth-child(3)').text().strip()  # 单位性质
                    _r['info']['SiteLicense'] = i('td:nth-child(4)').text().strip()  # 备案号
                    _r['info']['SiteName'] = i('td:nth-child(5)').text().strip()  # 网站名称
                    _r['info']['MainPage'] = i('td:nth-child(6) span').text().strip()  # 网站首页
                    _r['info']['VerifyTime'] = i('td:nth-child(7)').text().strip()  # 审核时间
        return result
    except Exception as e:
        logger.warn(e)
        return []

def _extract_filing_info_by_cnzz_mobile(domains):
    try:
        result = []
        base_url = "http://micp.chinaz.com/Icp/BatchSearchs/"
        _url = base_url
        if len(domains) == 0:
            logger.warn("not domain return!")
        _host = 'hosts='
        for _domain in domains:
            _result = {}
            _result['domain'] = _domain
            _result['info'] = {'CompanyName':'',
                    'CompanyType':'',
                    'MainPage':'',
                    'SiteLicense':'',
                    'SiteName':'',
                    'VerifyTime':'',
                    }
            result.append(_result)
            _host += "{}%0D%0A".format(_domain)
        resp = requests.post(_url,data= _host,headers=mobile_cnzz_headers)
        d = pq(resp.content)
        _info_list = d('table.table').items()
        for _info in _info_list:
            i = pq(_info)
            domain = i('thead tr td a').text().strip()
            for _r in result:
                if _r['domain'] == domain:
                    _r['info']['CompanyName'] = i('tbody tr:nth-child(1) td.z-tl').text().strip()  # 主办单位
                    _r['info']['CompanyType'] = i('tbody tr:nth-child(2) td.z-tl').text().strip()  # 单位性质
                    _r['info']['SiteLicense'] = i('tbody tr:nth-child(3) td.z-tl').text().strip()  # 备案号
                    _r['info']['SiteName'] = i('tbody tr:nth-child(4) td.z-tl').text().strip()  # 网站名称
                    _r['info']['MainPage'] = i('tbody tr:nth-child(5) td.z-tl').text().strip()  # 网站首页
                    _r['info']['VerifyTime'] = i('tbody tr:nth-child(6) td.z-tl').text().strip()  # 审核时间
        return result
    except Exception as e:
        logger.warn(e)
        return []

def batch_extract_filing_info(domains):
    '''
    备案信息查找，cnzz 设置每次最多查找20条数据
    :param domains:
    :return: [{'domain': '100credit.com',
               'info': {'organizer': '百融（北京）金融信息服务股份有限公司',
                        'type': '企业',
                        'filingnumber': '京ICP备14032774号-2',
                        'sitename': '百融金服官网',
                        'home': 'www.100credit.com',
                        'checktime': '2015/12/17 0:00:00',
                        'lasttime': '2019-03-19 21:16:27'}}]
    '''
    arg_list = []
    pool = ThreadPool(5)
    def _run_process(args):
        #_result = _extract_filing_info(args)
        _result = _extract_filing_info_by_cnzz_mobile(args) # cnzz mobile 接口 每次只能20个
        #print(_result)
        util.save_info(_result) # 保存数据
    domain_list = _list_of_groups(domains,20) # 按照200分割为小份
    if not domain_list:
        logger.warn("no domain return")
        return []
    for _domains in domain_list:
        arg_list.append(_domains)
    pool.map(_run_process, arg_list)
    pool.close()
    pool.join()

def _extract_filing_info_by_seos(domains):
    try:
        result = []
        base_url = "https://www.seos.vip/urlpla"

        _url = base_url
        if len(domains) == 0:
            logger.warn("not domain return!")
        _host = 'target='
        for _domain in domains:
            _result = {}
            _result['domain'] = _domain
            _result['info'] = {'CompanyName':'',
                    'CompanyType':'',
                    'MainPage':'',
                    'SiteLicense':'',
                    'SiteName':'',
                    'VerifyTime':'',
                    }
            result.append(_result)
            _host += "{}%0A".format(_domain)
        _host += "&beian_plnum=10000"
        resp = requests.post(_url,data= _host,headers=seos_headers,verify=False)
        j_result = resp.json()
        for i in j_result['list']:
            for _r in result:
                if i['onearr'] == _r['domain']:
                    if i.get("no") == 1:
                        return result
                    _r['info']['CompanyName'] = i.get("name")  # 主办单位
                    _r['info']['CompanyType'] = i.get("nature")  # 单位性质
                    _r['info']['SiteLicense'] = i.get("bah")  # 备案号
                    _r['info']['SiteName'] = i.get("name")  # 网站名称
                    _r['info']['MainPage'] = i.get("weburl")  # 网站首页
                    _r['info']['VerifyTime'] = i.get("create_time")  # 审核时间

        return result
    except Exception as e:
        logger.warn(e)
        return []



def batch_extract_filing_info_by_seos(domains):
    '''
    备案信息查找，cnzz 设置每次最多查找20条数据
    :param domains:
    :return: [{'domain': '100credit.com',
               'info': {'organizer': '百融（北京）金融信息服务股份有限公司',
                        'type': '企业',
                        'filingnumber': '京ICP备14032774号-2',
                        'sitename': '百融金服官网',
                        'home': 'www.100credit.com',
                        'checktime': '2015/12/17 0:00:00',
                        'lasttime': '2019-03-19 21:16:27'}}]
    '''
    arg_list = []
    pool = ThreadPool(5)
    def _run_process(args):
        _result = _extract_filing_info_by_seos(args)
        util.save_info(_result) # 保存数据
    domain_list = _list_of_groups(domains,500) # 按照200分割为小份
    if not domain_list:
        logger.warn("no domain return")
        return []
    for _domains in domain_list:
        arg_list.append(_domains)
    pool.map(_run_process, arg_list)
    pool.close()
    pool.join()


def _list_of_groups(init_list, split_list_len):
    '''
    列表分割
    :param init_list: ['baidu.com','58.com','xx.com']
    :param split_list_len: 2
    :return: [['baidu.com','58.com'],['xx.com']]
    '''
    list_of_group = zip(*(iter(init_list),) *split_list_len)
    end_list = [list(i) for i in list_of_group]
    count = len(init_list) % split_list_len
    end_list.append(init_list[-count:]) if count !=0 else end_list
    return end_list


if __name__ == '__main__':
    logger.warn = print
    logger.info = print
    domains = []
    import sys
    import os

    if len(sys.argv) != 2:
        print("python3 icp_scraper.py [TARGET-FILE]")
        sys.exit()
    target_file = sys.argv[1]
    if os.path.exists(target_file):
        with open(target_file, "r") as f:
            domains = f.readlines()
            domains = [i.strip() for i in domains]
            batch_extract_filing_info(domains) # 批量爬虫
    else:
        print("target file not found")

    # with open("7wdomain.txt","r") as f:
    #     domains = f.readlines()
    #     domains = [i.strip() for i in domains]
    # domains = domains
    #batch_extract_filing_info(domains)
    #print(_extract_filing_info(["baidu.com"]))
    #batch_extract_filing_info(domains)
    #print(_extract_filing_info_by_seos(["baidu.com","0055avtt.com"]))
    #batch_extract_filing_info_by_seos(domains)
    # print(_extract_filing_info_by_cnzz_mobile(domains)) cnzz mobile接口
    #batch_extract_filing_info(domains)