"""
  RANDOM MEME PRANK
  
  Author: Israel Dryer
  Modified: 2020-08-09
  
  Description: Who says programming can't be fun? In this video, I’m going to show you how to troll your friends.. all with Python! 
    We're going to create a python program that scrapes random memes from the internet on a timer and then mails them to your 
    friends and co-workers... forever... until you stop it.

  Requirements
  - BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
  - Requests: https://2.python-requests.org/en/master/

  SMTP Mail Servers
    GMAIL ** see notes below
    - smtp.gmail.com
    - port 587
    OUTLOOK
    - smtp-mail.outlook.com
    - port 587
    YAHOO
    - smtp.mail.yahoo.com
    - port 587
    AOL
    - smtp.aol.com
    - port 587

    Gmail has locked things down pretty good with what it considers less secure apps. That would include access your 
    Gmail account from the smtplib library in Python. However, there is a work around. You can enable access from 
    "Less Secure Apps" by going to your Gmail account and enabling that feature. However, you should do this at your
    own peril, and after carefully reading the warnings on their site.
    
    https://support.google.com/accounts/answer/6010255?hl=en
"""
import time
import smtplib
from email.message import EmailMessage
import requests
from bs4 import BeautifulSoup

# message settings
BASE_URL = "https://imgflip.com/i/"
HTML_TEMPLATE = "<div><img src={}></div>"

# email settings
USERNAME = 'yourname@email.com'
PASSWORD = 'password'

SMTP_HOST = 'smtp-mail.outlook.com'
SMTP_PORT = 587
DELAY = 5 # seconds

def get_random_meme():
    """Extract image url from website"""
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        # for regular image
        img_url = 'https:' + soup.find('img', id='im')['src']
    except TypeError:
        # for gif/video
        img_url = 'https:' + soup.find('video', id='vid')['poster']
    return img_url

def create_message(recipients):
    """Create an html formatted email message"""
    img_url = get_random_meme()
    html_body = HTML_TEMPLATE.format(img_url)
    msg = EmailMessage()
    msg['From'] = 'yourname@email.com'
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "Get back to work!"
    msg.set_content(html_body, subtype='html')
    return msg

def send_random_memes(recipients):
    """Send a random meme to each recipient; repeat until finished"""
    server = smtplib.SMTP(host=SMTP_HOST, port=SMTP_PORT)
    server.starttls()
    server.login(USERNAME, PASSWORD)
    
    msg_cnt = 0
    
    while True:
        try:
            message = create_message(recipients)
            server.send_message(message)
            msg_cnt += 1
            print(f'Message: {msg_cnt}')
            time.sleep(DELAY)
        except KeyboardInterrupt:
            server.close()
            break

if __name__ == '__main__':
    print('Program started')

    recipients = ['some1@email.com', 'some2@email.com']
    send_random_memes(recipients)

    print('Program ended')
