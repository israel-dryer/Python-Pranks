"""
PYTHON PRANK - Spam your co-workers with repeated meme emails
By Israel Dryer | June 24, 2019

OVERVIEW
This is a FUN prank to pull on your friends... if they have a sense of humor! This script will send 
a random meme to your list of contacts every 60 seconds for as many iterations as you select.

Use the images that I've selected, or add your own. All you need to do is run this script in the 
same location as another folder called 'img' that contains the images that you would like to attach 
to the email.

PRO-TIP CONNECTING TO GMAIL
Gmail has locked things down pretty good with what it considers "less secure" apps. That would 
include access your Gmail account from the `smtplib` library in Python. However, there is a work 
around. You can enable access from "Less Secure Apps" by going to your Gmail account and enabling 
that feature. However, you should do this at your own peril, and after carefully reading the 
warnings from the link below: https://support.google.com/accounts/answer/6010255

REFERENCES
- Email examples and libraries: https://docs.python.org/3.7/library/email.examples.html
- time.sleep(): https://docs.python.org/3.7/library/time.html#time.sleep
- random.randint(): https://docs.python.org/3/library/random.html#random.randint
- os.listdir(): https://docs.python.org/3/library/os.html#os.listdir

"""
### import project libraries
import os
import smtplib
import random
import time
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

### setup server authentication
username = 'user.name@gmail.com'
password = 'pas$w0rd'
fr_address = 'me@gmail.com'
to_address = 'you1@gmail.com, you2@gmail.com, you3@gmail.com'
smtp_host = 'smtp.gmail.com'

### setup message
subject = 'Get BACK to WORK!!'
message = 'What do you think you\'re doing?'
num_of_msg = 10 

### create and send the message
# get a list of all images in the img directory
memes = os.listdir('img')

# reference the image in the IMG SRC attribute by the ID we give it below
msgText = MIMEText(f'<b><i>{message}</i></b><br><br><img src="cid:image1">', 'html')

for i in range(num_of_msg):
    
    # random number generator for meme selection
    rand_num = random.randint(0,len(memes)-1)
    attachment = 'img/' + memes[rand_num]

    # create the message and fill in the from, to, and subject headers
    msg = MIMEMultipart('related')
    msg['From'] = fr_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(msgText)

    # open the attachment chosen above
    with open(attachment, 'rb') as img:
        msgImage = MIMEImage(img.read())

    # define the image's ID as referenced above
    msgImage.add_header('Content-ID', '<image1>')
    msg.attach(msgImage)

    # send the email
    server = smtplib.SMTP(host=smtp_host, port=587)
    server.starttls()
    server.login(username, password)
    server.send_message(msg)
    server.close()
    
    # wait 60 seconds before looping
    time.sleep(60)