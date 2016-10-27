import time
import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import datetime

user_id = lms아이디
user_pwd = lms비밀번호
email_adresses = [이메일주소들 입력]

data_lms = ['lms 초기값']
data_snue = ['snue 초기값']
send_lms_notice = ''
send_snue_notice = ''

def check_lms():
    payload = {
        'usr_id': user_id,
        'usr_pwd': user_pwd
    }
    with requests.Session() as s:
        s.post('http://lms.snue.ac.kr/ilos/lo/login.acl', data=payload)
        print("lms logged in")
        html = s.get('http://lms.snue.ac.kr/ilos/mp/mypage_main_list.acl')
        soup = BeautifulSoup(html.text, 'html.parser')
        urls = soup.select(
            'a.site-link'
        )
        lms_notice = []
        for i, url in zip(range(len(urls)), urls):
            if i % 3 == 0:
                new_list = []
                new_list.append(url.text)
            if i % 3 == 1:
                new_list.append(url.text+" 교수님")
            if i % 3 == 2:
                new_list.append(url.text.lstrip()+'\n')
                full_lms = "\n".join(new_list)
                lms_notice.append(full_lms)
    print ("lms parsing complete")
    original_lms_notice = lms_notice[:]
    global data_lms
    for original in data_lms:
        if original in lms_notice:
            lms_notice.remove(original)
    new_lms_notice = lms_notice[:]
    if new_lms_notice:
        print("새 공지 있음")
        if len(new_lms_notice) > 1:
            for i in range(len(new_lms_notice)):
                notice = str(i+1) + '. \n' + new_lms_notice.pop(0)
                new_lms_notice.append(notice)
        del data_lms[:]
        data_lms.extend(original_lms_notice)
        global send_lms_notice
        send_lms_notice = 'e-Class\n\n' + '\n'.join(new_lms_notice)
    else:
        print("새 공지 없음")
        send_lms_notice = ""
    print("\n")


def check_snue():
    r = requests.get('http://portal.snue.ac.kr/enview/board/list.brd?boardId=graduate_notice')
    snue_soup = BeautifulSoup(r.text, 'html.parser')
    snues = snue_soup.select(
        'td.td2'
    )
    snue_notice = []
    for snue in snues:
        snue_notice.append(snue.text.strip().lstrip()+'\n')
    print("snue parsing complete")
    original_snue_notice = snue_notice[:]
    global data_snue
    for original in data_snue:
        if original in snue_notice:
            snue_notice.remove(original)
    new_snue_notice = snue_notice[:]
    if new_snue_notice:
        print("새 공지 있음")
        #기존 공지를 새로 업데이트
        del data_snue[:]
        data_snue.extend(original_snue_notice)
        #새 공지가 1개보다 많으면 번호를 붙인다
        if len(new_snue_notice) > 1:
            for i in range(len(new_snue_notice)):
                notice = str(i+1) + '. \n' + new_snue_notice.pop(0)
                new_snue_notice.append(notice)
        global send_snue_notice
        send_snue_notice = '학사공지\n\n' + '\n'.join(new_snue_notice)
    else:
        print("새 공지 없음")
        send_snue_notice = ""
    print("\n")

def send_mail(notice1, notice2):
    # Specifying the from and to addresses
    fromaddr = 'test.smtp.lms@gmail.com'




    # Writing the message (this message will appear in the email)

    msg = ("{}\n{}").format(notice1, notice2).encode('utf-8')
    # Gmail Login

    username = 'test.smtp.lms@gmail.com'
    password = 'lmstest1'

    # Sending the mail

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    print("google logged in")

    for toaddrs in email_adresses:
        server.sendmail(fromaddr, toaddrs, msg)
        print("sent an alert mail")
    #send same email to each people
    server.quit()
    #smtp

def send_notice():
    global send_lms_notice, send_snue_notice
    try:
        print(datetime.datetime.today())
        check_lms()
        check_snue()
        if send_lms_notice or send_snue_notice:
            send_mail(send_lms_notice, send_snue_notice)
        print("next check after 10 minutes\n")
    except IndexError:
        print("로그인(인덱스) 에러ㅜㅜ\n20분 후에 다시 시도할게요!")
        time.sleep(1200)
        send_notice()

print("Initial check")
print(datetime.datetime.today())
check_lms()
check_snue()
print("next check after 10 minutes")
schedule.every(10).minutes.do(send_notice)

while True:
    schedule.run_pending()
    time.sleep(1)
