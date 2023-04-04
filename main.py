import requests
import base64
import time
from apscheduler.schedulers.blocking import BlockingScheduler

from config import verify_code_params, verify_code_headers, lecture_headers, lecture_key


def parse_verify_code(img_base64):
    """
    解析验证码

    Args:
        img_base64 (bytes): 验证码图片的base64字节码

    Returns:
        str: 解析的验证码
    """
    
    verify_code_params['file_base64'] = img_base64
    
    r = requests.post(
        url='http://upload.chaojiying.net/Upload/Processing.php', 
        data=verify_code_params, 
        headers=verify_code_headers,
    )
    res = r.json()

    if res['err_no'] == 0:
        return res['pic_str']
    else:
        print(f"解析验证码出错: {res['err_str']}")
        return None

def get_target_lecture(key):
    """
    获取目标讲座信息

    Args:
        key (str): 讲座名称关键词

    Returns:
        dict: 讲座数据
    """
    
    r = requests.post(
        url='http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/modules/hdyy/queryActivityList.do',
        headers=lecture_headers,
    )
    if r.status_code != 200 or len(r.text) == 0:
        print("讲座列表接口响应不成功，请检查cookie！")
        return None
  
    res = r.json()  
    lecture_list = res['datas']['hdlbList']
    if lecture_list is None or len(lecture_list) == 0:
        print("当前没有任何讲座可预约！")
        return None
    
    target_list = []
    for item in lecture_list:
        if key in item['JZMC']:
            target_list.append(item)
    
    if len(target_list) == 0:
        print("当前关键词没有搜索到任何讲座！")
        return None
    
    if len(target_list) > 1:
        print("注意！当前关键词可搜索到多个讲座，请指定更详细的关键词，或默认选择匹配的最后一项")
    
    return target_list[-1]

def get_lecture_verify_code(wid):
    """
   获取指定讲座的验证码

    Args:
        wid (str): 讲座id
        
    Returns:
        bytes: 验证码图片的base64字节码
    """
    
    r = requests.get(
        url='http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/modules/hdyy/vcode.do',
        params={'_': int(time.time() * 1000)},
        headers=lecture_headers,
    )
    res = r.json()
    
    base64_str = res['datas']
    base64_str = base64_str[(base64_str.index("base64,") + 7):]
    return bytes(base64_str, encoding='utf-8')

def reserve_lecture(wid, verify_code):
    """
   预约指定讲座

    Args:
        wid (str): 讲座id
        verify_code (str): 验证码
    
    Returns:
        bool: 预约结果
    """
    
    params = {
        'wid': wid,
        'vcode': verify_code,
    }
    r = requests.post(
        url='http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/modules/hdyy/addReservation.do',
        data=params,
        headers=lecture_headers,
    )

    res = r.json()
    print('预约接口响应数据: ', res)
    
    return res['code'] == 0 and res['datas'] == 1
    
def keep_alive(wid):
    """
    获取指定讲座信息以保活

    Args:
        wid (str): 讲座id
    """
    
    r = requests.post(
        url='http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/modules/hdyy/getActivityDetail.do',
        data={ 'wid': wid },
        headers=lecture_headers,
    )
    res = r.json()
    if res['code'] != 0:
        print('保活失效，请检查cookie！')
    
    print('用户身份有效，登录状态保活')
    
def rob(wid):
    """
    定时抢讲座任务

    Args:
        wid (str): 讲座id
    """
    
    print("定时预约任务开始, wid: ", wid)
    # 获取验证码图片
    verify_code_img_base64 = get_lecture_verify_code(wid)
    # 解析验证码
    verify_code = parse_verify_code(verify_code_img_base64)
    print("解析验证码成功: ", verify_code)
    # 尝试预约讲座
    res = reserve_lecture(wid, verify_code)
    print("预约结果: ", res)
    

if __name__ == "__main__":
    # 先在config中修改用户cookie和目标讲座名称！
    
    # 获取目标讲座信息
    lecture = get_target_lecture(lecture_key)
    if lecture is None:
        exit(1)
    
    print('搜索到目标讲座: ', lecture['JZMC'])
    
    # 立即检查一次保活
    keep_alive(lecture['WID'])
    
    # 启动定时任务
    scheduler = BlockingScheduler()
    scheduler.add_job(keep_alive, 'interval', seconds=30, args=[ lecture['WID'] ])
    scheduler.add_job(rob, 'cron', hour=19, minute=0, second=1, args=[ lecture['WID'] ])
    scheduler.start()
    