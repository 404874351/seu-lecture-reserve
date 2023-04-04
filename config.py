# 验证码解析参数
verify_code_params = {
    'user': '<your-username>',
    'pass': '<your-password>',
    'softid': '<your-softid>',
    'codetype': 1902,
    'file_base64': ''
}

# 验证码解析请求头
verify_code_headers = {
    'Connection': 'Keep-Alive',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
}

# 讲座系统请求头
lecture_headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'Host': 'ehall.seu.edu.cn',
    'Origin': 'http://ehall.seu.edu.cn',
    'Referer': 'http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/*default/index.do',
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    'X-Requested-With': 'XMLHttpRequest',
    # 每次操作前修改cookie
    'Cookie': '<your-cookie>'
}

# 目标讲座关键词，请尽可能指向唯一目标
lecture_key = "<lecture-title>"