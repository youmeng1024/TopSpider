import requests
import json
def request_get(url,params=None):
    result = requests.get(url,params=params,cookies=cookieFactory,headers=theheaders)
    return result

def request_post(url,datas=None,params=None):
    result = requests.post(url,data=json.dumps(datas),params=params,cookies=cookieFactory,headers=theheaders)
    return result


target_url = "http://bjx.iimedia.cn/app_rank"
result = requests.get(target_url)
cookieFactory = result.cookies
theheaders={
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "bjx.iimedia.cn",
    "Referer": "http://bjx.iimedia.cn/app_rank",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}


#http://bjx.iimedia.cn/applicationMonth获取
mouth_url = "http://bjx.iimedia.cn/applicationMonth"
mouth = request_get(mouth_url)

#http://bjx.iimedia.cn/applicationType分类数据获取..id=0为全部
appType = "http://bjx.iimedia.cn/applicationType"
appSort = request_get(appType)


#http://bjx.iimedia.cn/applicationRank?time=201908&offset=0&limit=20&main_type=0&sub_type=0&orderBy=0&order=0
#获取top列表名
list_url = "http://bjx.iimedia.cn/applicationRank"
params = {
    "time": 201908, #年月的数据
    "offset": 0, #数据偏移
    "limit": 200, #显示个数
    "main_type": 0,
    "sub_type": 0,
    "orderBy": 0,
    "order":0
}
list_result = request_get(list_url,params)
app_list = []
for item in list_result.json():
    app_list.append(item["app_name"])
print(app_list)


##############################################
#开始进行下载的爬虫
downURL = {}
for name in app_list:
    homeUrl = "https://sj.qq.com/myapp/"
    cookieFactory ={
    }
    theheaders={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "sj.qq.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    }

    homeResult = request_get(homeUrl)
    cookieFactory = homeResult.cookies

    #https://sj.qq.com/myapp/searchAjax.htm?kw=QQ&pns=&sid=获取搜索结果
    searchUrl = "https://sj.qq.com/myapp/searchAjax.htm"
    params = {
        "kw": name,
         "pns": "",
         "sid": "",
    }
    theheaders={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "sj.qq.com",
        "Origin": "https://sj.qq.com",
        "Referer": "https://sj.qq.com/myapp/search.htm?kw=",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36",
    }
    targetList = request_post(searchUrl,params,params)
    for infoList in targetList.json()['obj']['appDetails']:
        if infoList['appName'] == name:
            downURL[name] = infoList['apkUrl']
            break
    print(name+"--"+infoList['apkUrl'])
print(downURL)