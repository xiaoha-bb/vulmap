from pymongo import MongoClient

# 数据库参数
DB_HOST = '47.243.106.13'  # MongoDB Host
DB_PORT = 3306  # MongoDB Port (int)
DB_NAME = 'haiguandb'  # MongoDB Name
DB_PASSWROD = 3306  # MongoDB Port (int)
FILING_COLLECTION = 'domain_filing'
WHOIS_COLLECTION = 'domain_whois'
f = open("no_whois_domain","a+")

"http://tianjin.customs.gov.cn/"

"""
   数据库操作
"""
client = None

def conn_db(collection):
    global client
    if client == None:
        client = MongoClient(DB_HOST, DB_PORT)

    db = client[DB_NAME]
    collection = db[collection]
    return collection

def save_info(data):
    if not data:
        return
    for _info in data:
        if not _info['info'].get('CompanyName'):
            print(_info.get('domain'))
            continue
        item = {
            'domain':_info['domain'],
            'filing_info':_info['info']
        }
        if _info.get("domain"):
            r = conn_db(FILING_COLLECTION).delete_one({"domain":_info['domain']}) # 删除旧数据
            if r.deleted_count:
                print("remove {} success".format(_info.get('domain')))

        connect_id = conn_db(FILING_COLLECTION).insert_one(item).inserted_id
        if connect_id:
            try:
                print(connect_id)
            except Exception as e:
                print("{}".format(e))

def save_whois_info(data):
    if not data:
        return
    if not data['info']:
        print("maybe not whois "+data['domain'])
        f.write(str(data['domain'])+"\n")
        return
    item = {
        'domain':data['domain'],
        'whois_info':data['info']
    }
    if data.get("domain"):
        r = conn_db(WHOIS_COLLECTION).delete_one({"domain":data['domain']}) # 删除旧数据
        if r.deleted_count:
            print("remove {} success".format(data['domain']))
    connect_id = conn_db(WHOIS_COLLECTION).insert_one(item).inserted_id
    if connect_id:
        try:
            print(item)
        except Exception as e:
            print("{} {}".format(item["domain"],e))
