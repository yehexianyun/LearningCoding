# -*- coding: utf-8 -*-
#%%准备
import time,re,requests,os,pickle
#该pickle文件包含每一上市公司公告的下载地址，标题，时间，公司代码，公司名称。
with open(file = "../Announcements_SSE_Dataframe.pkl", mode = "rb") as f:
    sse_df = pickle.load(file = f)
f.close()
#数据预处理
#代码列表存在股票代码与债券代码合并的情况。以下过程提取股票代码
for index, col in sse_df.items():
    if (col.apply(lambda x: isinstance(x, list)).all()): #如果该列的每个元素都是list，则提取list中的第一个元素转换为字符串。
        sse_df[index] = sse_df[index].apply(lambda x: x[0]) 
sse_df = sse_df.sort_values(by = ["SECURITY_CODE", "SSEDATE"]).reset_index(drop = True) #排序以使数据规整

#定义headers
sse_download_headers = {"Host": "static.sse.com.cn",
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip,deflate,br",
                        "DNT": "1",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Cache-Control": "max-age=0",
                        "TE": "Trailers"}

#定义获取代理IP的函数
def GetIpPort():
    #优亦云免费代理，每日500个免费IP，每次最多获取1个IP，每秒最多获取1个IP
    url_yyy_free = "http://data.yyyip.cn:8888/pick_api?token=A76BC5E50C4777FA87A154960298BF22&upid=5209&count=1&protocol=1&iptype=1017&datatype=1&operators=0&repeat=0&area=0"
    #优亦云付费代理，每次最多获取1个IP，每秒最多获取1个IP
    url_yyy_nonfree = "http://data.yyyip.cn:8888/pick_api?token=A76BC5E50C4777FA87A154960298BF22&upid=5229&count=1&protocol=1&iptype=1000&datatype=1&operators=0&repeat=0&area=0"
    #四叶天付费代理，支持高并发
    url_syt = "http://proxy.siyetian.com/apis_get.html?token=AesJWLNpXR55ERJdXTq10dNpXQ14EVJlnTB1STqFUeNpXQ61ERrBTTUVUMOp2Z31kaNNTTEVFe.AO0EzN2kzMxcTM&limit=1&type=0&time=10&split=1&split_text="
    tmp = requests.get(url = url_yyy_free).text.strip()
    if not re.match(pattern = "^(\d{1,3}\.){3}\d{1,3}:\d+$", string = tmp):
        while re.search(pattern = "最高调用频率为1秒", string = tmp):
            time.sleep(1)
            tmp = requests.get(url = url_yyy_free).text.strip()
    if not re.match(pattern = "^(\d{1,3}\.){3}\d{1,3}:\d+$", string = tmp):
        if re.search(pattern = "该套餐今日IP已用完", string = tmp):
            tmp = requests.get(url = url_yyy_nonfree).text.strip()
    if not re.match(pattern = "^(\d{1,3}\.){3}\d{1,3}:\d+$", string = tmp):
        while re.search(pattern = "最高调用频率为1秒", string = tmp):
            time.sleep(1)
            tmp = requests.get(url = url_yyy_nonfree).text.strip()
    if not re.match(pattern = "^(\d{1,3}\.){3}\d{1,3}:\d+$", string = tmp):
        if re.search(pattern = "套餐ID错误，该套餐不存在或已过期", string = tmp):
            tmp = requests.get(url = url_syt).text.strip()
    if not re.match(pattern = "^(\d{1,3}\.){3}\d{1,3}:\d+$", string = tmp):
        tmp = None
    return tmp

#%%下载

ip_port = GetIpPort() #获取代理IP
#分片运行，每个切片下载100000个文件
for row in sse_df.iloc[:100000, ].itertuples(): 
    file_folder = "./SSE/" + row.SECURITY_CODE + "/"
    #命名规则，索引+1_公司代码_日期_标题.后缀，标题中的非法字符将被替换为下划线，文件夹不存在时创建文件夹。由于重复条目，使用复杂名称
    file_name = str(row.Index + 1) + \
                "_" + row.SECURITY_CODE + \
                "_" + row.SSEDATE + \
                "_" + re.sub(pattern = '[\\\\/:*?"<>|\s]', repl = "_", string = repr(row.TITLE.strip(" ")))[1:-1] + \
                "." + row.URL.split(".")[-1].lower()
    file_path = file_folder + file_name
    if not os.path.isfile(file_path):
        time.sleep(1)
        print("\r  Downloading: " + str(row.Index + 1) + " / " + str(sse_df.shape[0]) + "  |  " + file_name, end = "")
        res = None
        #尝试3次下载，下载失败则跳过
        cnt = 0
        while not (res != None and res.status_code == 200):
            try:
                cnt += 1
                res = requests.get(url = row.URL,
                                   headers = sse_download_headers,
                                   timeout = 3,
                                   proxies = {"http": ip_port, "https": ip_port})
            except Exception:
                ip_port = GetIpPort()
            if cnt >= 3:
                break
        if res != None and res.status_code == 200:
            os.makedirs(file_folder, exist_ok=True)
            with open(file=file_path, mode="wb") as f:
                f.write(res.content)
            f.close()
            print("\r  Downloading: " + str(row.Index + 1) + " / " + str(
                sse_df.shape[0]) + "  |  " + file_name + "  ------------  localization completed!", end="")
        else: #应对ip获取失败导致的循环终止
            print("\r  Downloading: " + str(row.Index + 1) + " / " + str(
                sse_df.shape[0]) + "  |  " + file_name + "  ------------  skipped!", end="")
    else: #文件已存在
        print("\r  Downloading: " + str(row.Index + 1) + " / " + str(sse_df.shape[0]) + "  |  " + file_name + "  ------------  already localized!", end = "")

