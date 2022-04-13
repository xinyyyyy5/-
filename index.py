import requests
import json
import time
import hashlib
import yaml
import random
import yagmail
from datetime import datetime, timedelta, timezone
from tkinter import *
import webbrowser
from PIL import Image,ImageTk
yag = yagmail.SMTP(user='2448341003@qq.com', password='mnjhucmzhrcodjgi', host='smtp.qq.com')
# Generate table Randomly
alphabet = list('abcdefghijklmnopqrstuvwxyz')
random.shuffle(alphabet)
table = ''.join(alphabet)[:10]

def getTimeStr():
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    return bj_dt.strftime("%Y-%m-%d %H:%M:%S")
def MD5(s):
    return hashlib.md5(s.encode()).hexdigest()


def encrypt(s):
    result = ''
    for i in s:
        result += table[ord(i) - ord('0')]
    # print(result)
    return result


def Run(IMEI,email):


    API_ROOT = 'http://client3.aipao.me/api'  # client3 for Android
    Version = '2.40'

    # Login
    TokenRes = requests.get(
        API_ROOT + '/%7Btoken%7D/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI,headers={"version":"2.40"})
    TokenJson = json.loads(TokenRes.content.decode('utf8', 'ignore'))
    # print(TokenJson)

    if not TokenJson['Success']:
        print('IMEI过期了')
        yag.send(to=email, subject='晨跑通知',
                 contents=getTimeStr() + '   ' +'IMEI已过期或者IMEI输入错误（阳光体育每七天需要重新登录一次，IMEI码随之也会更换，请检查IMEI）')
        # exit(0)

    # print(TokenJson)

    # headers
    token = TokenJson['Data']['Token']
    userId = str(TokenJson['Data']['UserId'])
    timespan = str(time.time()).replace('.', '')[:13]
    auth = 'B' + MD5(MD5(IMEI)) + ':;' + token
    nonce = str(random.randint(100000, 10000000))
    sign = MD5(token + nonce + timespan + userId).upper()  # sign为大写

    header = {'nonce': nonce, 'timespan': timespan,
              'sign': sign, 'version': Version, 'Accept': None, 'User-Agent': None, 'Accept-Encoding': None,
              'Connection': 'Keep-Alive'}

    # Get User Info

    GSurl = API_ROOT + '/' + token + '/QM_Users/GS'
    GSres = requests.get(GSurl, headers=header, data={})
    GSjson = json.loads(GSres.content.decode('utf8', 'ignore'))

    Lengths = GSjson['Data']['SchoolRun']['Lengths']

    print('User Info:', GSjson['Data']['User']['UserID'], GSjson['Data']['User']['NickName'],
          GSjson['Data']['User']['UserName'], GSjson['Data']['User']['Sex'])
    print('Running Info:', GSjson['Data']['SchoolRun']['Sex'], GSjson['Data']['SchoolRun']['SchoolId'],
          GSjson['Data']['SchoolRun']['SchoolName'], GSjson['Data']['SchoolRun']['MinSpeed'],
          GSjson['Data']['SchoolRun']['MaxSpeed'], GSjson['Data']['SchoolRun']['Lengths'])

    # Start Running
    SRSurl = API_ROOT + '/' + token + \
             '/QM_Runs/SRS?S1=31.899029&S2=118.908211&S3=' + str(Lengths)
    SRSres = requests.get(SRSurl, headers=header, data={})
    SRSjson = json.loads(SRSres.content.decode('utf8', 'ignore'))

    # print(SRSjson)

    # Generate Runnig Data Randomly
    RunTime = str(random.randint(300, 400))  # seconds
    RunDist = str(Lengths + random.randint(0, 3))  # meters
    RunStep = str(random.randint(550, 650))  # steps

    # print(RunTime,RunStep,RunDist)

    # Running Sleep
    # StartT = time.time()
    # for i in range(int(RunTime)):
    #     time.sleep(1)
    #     # print("test")
    #     print(f"Current Minutes: {i/60:.2f} Running Progress {i*100.0/int(RunTime):.2f}")
    # print("")
    # print("Running Seconds:", time.time() - StartT)

    # print(SRSurl)
    # print(SRSjson)

    RunId = SRSjson['Data']['RunId']

    # End Running
    EndUrl = API_ROOT + '/' + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
             encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
             '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep)

    EndRes = requests.get(EndUrl, headers=header)
    EndJson = json.loads(EndRes.content.decode('utf8', 'ignore'))

    print("-----------------------")
    print("Time:", RunTime)
    print("Distance:", RunDist)
    print("Steps:", RunStep)
    print("-----------------------")

    print(EndJson)

    if (EndJson['Success']):
                 print('success !!!')
                 yag.send(to=email,subject='晨跑通知',contents=getTimeStr() + '   ' + '自动晨跑成功,若不在规定时间内，则为无效记录哦')
    else:
                print('fail!!!')
                yag.send(to=email, subject='晨跑通知',contents=getTimeStr() + '   ' + '由于未知原因，很遗憾，自动晨跑失败了')
def main():
 root = Tk()
 root.title('阳光体育晨跑一键刷')
 root.geometry('300x150')
 root.resizable(0,0)
 Label(root, text='请输入你的IMEI:', font=("华文行楷", 10), fg='pink',bg='#d3fbfb').grid(row=1,sticky=W)
 E1 = Entry(root,font=("华文行楷",10),fg='pink',bg='#d3fbfb')
 E1.grid(row=1, column=1)
 Label(root, text='请输入你的邮箱:', font=("华文行楷", 10), fg='pink',bg='#d3fbfb').grid(row=3,column=0,sticky=W)
 E2 = Entry(root,font=("华文行楷",10),fg='pink',bg='#d3fbfb',)
 E2.grid(row=3,column=1,sticky=W)
 def main_handler():
     Run(E1.get(), E2.get())
 def chaxun():
     webbrowser.open("https://www.bilibili.com/video/BV1cA411M75Y?from=search&seid=555839192045415207")
     webbrowser.open("https://www.bilibili.com/video/BV1sy4y1z7s8/?spm_id_from=333.788.recommend_more_video.-1")
 Button(root, text='一键秒刷', font=("微软雅黑", 10),fg='pink',bg='#d3fbfb', height=1,width=7,command=main_handler).grid(row=5,column=1)
 Button(root,text='获取IMEI教程',font=("微软雅黑",10),fg='pink',bg='#d3fbfb',command=chaxun).grid(row=5,column=0)
 Message(root,text='author：小新QAQ Q：2448341003,点击一键秒刷后请去邮箱查看刷跑信息').grid(row=6,column=1)
 image1=PhotoImage(file="1.gif")
 Label(root,image=image1,width=120,height=70).grid(row=6,column=0)
 mainloop()
if __name__ == '__main__':
    main()
