import datetime
import requests
from bs4 import BeautifulSoup
import smtplib
import re
import schedule
import time

email_adresses = [받을 이메일주소 입력]

def send_mail(menu_food):
    # Specifying the from and to addresses
    print(menu_food)
    # Specifying the from and to addresses
    fromaddr = 'test.smtp.lms@gmail.com'

    # Writing the message (this message will appear in the email)

    msg = ("Subject: 오늘의 학식메뉴~!\n" + "Today's Menu : \n" + menu_food).encode('utf-8')

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
    server.quit()
    #smtp

day_menu = []
def check_food():
    r = requests.get('http://portal.snue.ac.kr/enview/2015/food.jsp')
    food_soup = BeautifulSoup(r.text, 'html.parser')
    food_menus = food_soup.select(
        'td'
    )
    a = 1
    del day_menu[:]
    for menu in food_menus:
        menu = menu.text
        if a % 5 == 1 or a % 5 == 3:
            day_menu.append(menu)
        a += 1
    print(day_menu)

def really_send_mail():
    today = datetime.datetime.today().weekday()
    food_message = day_menu[today*2] + '\n' + day_menu[today*2 + 1]
    print(today)
    if today < 5:
        send_mail(food_message)

print("학식 알림 서비스 시작")
check_food()

schedule.every().monday.at('00:11').do(check_food)
schedule.every().day.at("08:30").do(really_send_mail)

while True:
    schedule.run_pending()
    time.sleep(1)
