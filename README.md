# seu-lecture-reserve

#### 介绍

东南大学讲座预约半自动脚本，适用于图片验证码方式

#### 接口账户配置

由于脚本需要自动获取验证码图片，并识别验证码，因此选用超级鹰接口服务。其账户配置过程如下：

1. 访问 http://www.chaojiying.com/ ，注册账号，充值1元作为接口费用。
2. 进入个人中心 > 软件ID，申请一个软件ID。
3. 将用户名，密码，软件ID分别复制到 config.py 中的 verify_code_params['user']，verify_code_params['pass']，verify_code_params['softid']

#### 脚本使用

1. 浏览器访问 http://ehall.seu.edu.cn/gsapp/sys/yddjzxxtjappseu/*default/index.do#/hdyy 。
2. 在网页中右键或按F12进入控制台，复制请求头中的 cookie 到 config.py 中的 lecture_headers['Cookie'] 。
3. 寻找需要预约的讲座名称，截取标题中的部分复制到 config.py 中的 lecture_key 。
4. （可选）设置 main.py 中177行的定时预约任务触发时间，默认常用时间为19:00:01。
5. 在讲座预约时间开始前10分钟内，运行 main.py ，待讲座预约成功控制台将输出相关信息。


