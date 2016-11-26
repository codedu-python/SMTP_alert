import time
import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import datetime

user_id = input('E-class 아이디')
user_pwd = input('E-clas 비밀번호')

data_lms = ['lms 초기값']
data_snue = ['snue 초기값']

def check_lms():
    payload = {
        'usr_id': user_id,
        'usr_pwd': user_pwd
    }
    with requests.Session() as s:
        s.post('http://lms.snue.ac.kr/ilos/lo/login.acl', data=payload)
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
    original_lms_notice = lms_notice[:]
    global data_lms
    for original in data_lms:
        if original in lms_notice:
            lms_notice.remove(original)
    new_lms_notice = lms_notice[:]
    if 0< len(new_lms_notice) < 11:
        print("lms 새 공지 있음")
        if len(new_lms_notice) > 1:
            for i in range(1, len(new_lms_notice)+1):
                notice = str(i) + '. \n' + new_lms_notice.pop(0)
                new_lms_notice.append(notice)
        del data_lms[:]
        data_lms.extend(original_lms_notice)
        send_lms = ('e-Class\nhttp://lms.snue.ac.kr/\n\n'
        + '\n'.join(new_lms_notice))
    elif len(new_lms_notice)>10:
        print("lms 새로운 공지가 10개 이상..?")
        for i in range(1, 11):
            notice = str(i) + '. \n' + new_lms_notice.pop(0)
            new_lms_notice.append(notice)
        del data_lms[:]
        data_lms.extend(original_lms_notice)
        send_lms = ('e-Class 새 공지 알림\n\n'
        + ''.join(new_lms_notice[10:]) + '\n링크 : http://lms.snue.ac.kr/')
    else:
        print("lms 새 공지 없음")
        send_lms = ""
    return send_lms


def check_snue():
    r = requests.get('http://portal.snue.ac.kr/enview/board/list.brd?boardId=graduate_notice')
    snue_soup = BeautifulSoup(r.text, 'html.parser')
    snues = snue_soup.select(
        'td.td2'
    )
    snue_notice = []
    for snue in snues:
        snue_notice.append(snue.text.strip().lstrip()+'\n')
    original_snue_notice = snue_notice[:]
    global data_snue
    for original in data_snue:
        if original in snue_notice:
            snue_notice.remove(original)
    new_snue_notice = snue_notice[:]
    if new_snue_notice:
        print("학사공지 새 공지 있음")
        #기존 공지를 새로 업데이트
        del data_snue[:]
        data_snue.extend(original_snue_notice)
        #새 공지가 1개보다 많으면 번호를 붙인다
        if len(new_snue_notice) > 1:
            for i in range(len(new_snue_notice)):
                notice = str(i+1) + '. \n' + new_snue_notice.pop(0)
                new_snue_notice.append(notice)
        send_snue = '학사공지 새 공지 알림\n\n' + ''.join(new_snue_notice) + '\n링크 : http://www.snue.ac.kr/muskSquare/index.do?sub_no=4&sub_one_dept_no=0&sub_two_dept_no=1'
    else:
        print("학사공지 새 공지 없음")
        send_snue = ""
    return send_snue


data_ebook = ['이북 도서 초기값']
data_library = ['도서관 도서 초기값']
def ebook_parser(page_url, booklist):
    p = requests.get(page_url)
    ebook_soup = BeautifulSoup(p.text, 'html.parser')
    ebooks = ebook_soup.select('a')
    authors = ebook_soup.select('em')
    for ebook, author in zip(ebooks[50:64:3], authors[11::2]):
        booklist.append(ebook.text + '\n' + author.text.lstrip().strip())
def check_ebook():
    booklist = []
    for i in range(1, 4):
        ebook_parser("http://ebook.snue.ac.kr/Kyobo_T3/Content/Content_Best_List.asp?product_cd=&category_id=&content_all=Y&order_key=BORROW_CNT&search_keyword=&search_type=&search_product_cd=&list_type=N&now_page={}".format(i), booklist)
    original_booklist = booklist[:]
    global data_ebook
    for original in data_ebook:
        if original in booklist:
            booklist.remove(original)

    new_booklist = booklist[:]
    if new_booklist:
        print("이북 새 도서 있음")
        #기존 공지를 새로 업데이트
        del data_ebook[:]
        data_ebook.extend(original_booklist)
        #새 공지가 1개보다 많으면 번호를 붙인다
        if len(booklist) > 1:
            for i in range(len(booklist)):
                book = str(i+1) + '. \n' + new_booklist.pop(0)
                new_booklist.append(book)
        send_ebook = '이북 새 도서 알림\n\n' + '\n'.join(new_booklist) + '\n링크 : http://ebook.snue.ac.kr'
    else:
        print("이북 새 공지 없음")
        send_ebook = ""
    return send_ebook


def check_libbook():
    t = requests.get('http://www.lib.snue.ac.kr/search/Search.Result.ax?sid=7')
    lib_soup = BeautifulSoup(t.text, 'html.parser')
    libs = lib_soup.select('a.pyxisv4_title')
    booklist = []
    for lib in libs:
        if lib.text:
            booklist.append(lib.text.lstrip().strip())
    original_booklist = booklist[:]
    global data_library
    for original in data_library:
        if original in booklist:
            booklist.remove(original)

    new_booklist = booklist[:]
    if new_booklist:
        print("도서관 새 도서 있음")
        #기존 공지를 새로 업데이트
        del data_library[:]
        data_library.extend(original_booklist)
        #새 공지가 1개보다 많으면 번호를 붙인다
        if len(booklist) > 1:
            for i in range(len(booklist)):
                book = str(i+1) + '. \n' + new_booklist.pop(0)
                new_booklist.append(book)
        send_library = '도서관 새 도서 알림\n\n' + '\n'.join(new_booklist) + '\n링크 : http://lib.snue.ac.kr'
    else:
        print("도서관 새 공지 없음")
        send_library = ""
    return send_library



def send_mail():
    try:
        print(datetime.datetime.today())
        ebook_msg = check_ebook()
        libbook_msg = check_libbook()
        snue_msg = check_snue()
        lms_msg = check_lms()
        book_msg = ebook_msg + '\n\n' + libbook_msg
    except IndexError:
        print("lms 로그인(인덱스) 에러ㅜㅜ\n20분 후에 다시 시도할게요!")
        time.sleep(1200)
        send_mail()
    addresses = {'rhoetaek@gmail.com' :'\n\n\n'.join([snue_msg, lms_msg, book_msg]), 'juju11627@student.snue.ac.kr':'\n\n\n'.join([lms_msg, snue_msg]),
     'ksa9595@student.snue.ac.kr':'\n\n\n'.join([lms_msg, snue_msg]), 'tkdfl1219@gmail.com':'\n\n\n'.join([snue_msg, book_msg]), 'kyh112394@gmail.com' : '\n\n\n'.join([lms_msg, snue_msg, book_msg]), 'jinsoo0314@gmail.com':'\n\n\n'.join([lms_msg, snue_msg])}
    if libbook_msg or ebook_msg or snue_msg or lms_msg:
        # Specifying the from and to addresses
        fromaddr = 'test.smtp.lms@gmail.com'


        username = 'test.smtp.lms@gmail.com'
        password = 'lmstest1'

        # Sending the mail

        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,password)
        print("google logged in")
        for toaddrs in addresses.keys():
            if addresses[toaddrs].replace('\n', ''):
                msg = addresses[toaddrs]
                if addresses[toaddrs].startswith('\n\n\n'):
                    msg = addresses[toaddrs][3:]
                if addresses[toaddrs].startswith('\n\n\n\n\n\n'):
                    msg = addresses[toaddrs][6:]
                server.sendmail(fromaddr, toaddrs, msg.encode('utf-8'))
                print("sent an alert mail")
        #send same email to each people
        server.quit()
    print('next check after 10 minutes\n')


print("Initial check")
print(datetime.datetime.today())
check_libbook()
check_ebook()
check_snue()
check_lms()
print("next check after 10 minutes\n")
schedule.every(10).minutes.do(send_mail)

while True:
    schedule.run_pending()
    time.sleep(1)
