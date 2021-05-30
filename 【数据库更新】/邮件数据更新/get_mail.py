import imaplib
import poplib
import email
from email.header import decode_header
from email.parser import BytesParser
import os
from io import StringIO, BytesIO
import data_organize as do
import re
import datetime as dt
import data_organize as do

def decode_str(s):#字符编码转换
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def get_mail_pool(host, username, password, n=5):
    conn = imaplib.IMAP4_SSL(host = host)
    print('已连接服务器')
    conn.login(username, password)
    print('已登陆')
    # 上传客户端身份信息
    status, msgs = conn.select()
    resp, mails = conn.list()
    
    #typ, data = conn.search(None, 'ALL')

    typ, data = conn.search(None, '(FROM "marketdata@chinamoney.com.cn")')
    print("已经得到data")

    msg_list=[]
    count=0
    for num in data[0].split()[::-1]:#邮件编码
        typ, data_content = conn.fetch(num, '(RFC822)')
        text = data_content[0][1]#邮件内容
        msg = email.message_from_string(text.decode())   # 转换为email.message对象
        msg_list.append(msg)
        count += 1
        #if count > 10 :
        #    break
    return msg_list

def get_att(msg, download_io):
    attachment_files = []
    attachment_date=[]
    for part in msg.walk():
        file_name = part.get_filename()  # 获取附件名称类型
        # print(file_name)
        contType = part.get_content_type()
        
        if file_name:
            h = email.header.Header(file_name)
            dh = email.header.decode_header(h)  # 对附件名称进行解码
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))  # 将附件名称可读化
                # print("发现附件："+filename)
                # filename = filename.encode("utf-8")
            if  "现券市场"  in filename:
                data = part.get_payload(decode=True)  # 下载附件
                att_file = open(download_io + filename,"wb")
                # 在指定目录下创建文件，注意二进制文件需要用wb模式打开
                attachment_files.append(filename)
                att_file.write(data)  # 保存附件
                att_file.close()
      
    return attachment_files



def download_certain_mail(msg_list,download_io,lastday):
    try:
        subject_list=[]
        date_list=[]
        for msg in msg_list:
            # 获取可读的附件名
            subject=decode_str(msg.get("subject"))
            # print(subject)# 附件名

            # 查找邮件名中的八位数字
            date= re.search(r"\d{8}",subject)[0]
                     
            if "现券" in subject and date > lastday.strftime("%Y%m%d") :
                subject_list.append(subject)
                date_list.append(date)
                get_att(msg,download_io)
                print("已经下载附件："+subject)
            else:
                pass
            
    except BaseException as e:
        print('fail error:',e)


def main():
    # 附件下载路径
    download_io = "/Users/wdt/Desktop/tpy/raw_data_pool/现券市场交易情况总结/日报/"
    
    # @ 读取mail_config.txt内的邮箱信息
    io=os.getcwd() + "/mail_config.txt"
    with open(io, 'r') as f1:
        config = f1.readlines()
    for i in range(0, len(config)):
        config[i] = config[i].rstrip('\n')
    host = config[0]  # pop.163.com
    username = config[1]  # 用户名 
    password = config[2]  # 密码

    # 获取数据库内最后更新时间
    last_date = do.get_latest_date('Net_buy_bond')

    #获取邮件池子
    msg_list = get_mail_pool(host,username,password)
    #下载邮件
    download_certain_mail(msg_list,download_io, last_date)

if __name__ == "__main__":
    main()