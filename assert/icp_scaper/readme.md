### whois 信息爬取
`python3 whois_scraper.py [TARGET-FILE]`

### filing 备案信息爬取
`python3 icp_scraper.py [TARGET-FILE] `


### 数据库配置
```
util.py文件中修改
# 数据库参数
DB_HOST = '127.0.0.1'  # MongoDB Host
DB_PORT = 27017  # MongoDB Port (int)
DB_NAME = 'arl_z'  # MongoDB Name
FILING_COLLECTION = 'domain_filing'
WHOIS_COLLECTION = 'domain_whois'
```

### 数据导出
```
mongoexport --db arl_z --collection domain_filing --out 7w_filing.json
mongoexport --db arl_z --collection domain_whois --out 7w_whois.json
```
