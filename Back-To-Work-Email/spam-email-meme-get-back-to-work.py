"""
PYTHON PRANK - Spam your co-workers with repeated meme emails
By Israel Dryer | June 24, 2019

OVERVIEW
This is a fun prank** to pull on your friends, if they have a sense of humor! This script will send 
a random meme to a list of recipients every 60 seconds for as many times as you indicate.

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
- smtplib: https://docs.python.org/3/library/smtplib.html#module-smtplib
- email.meme.multipart: https://docs.python.org/3.7/library/email.mime.html#email.mime.multipart.MIMEMultipart
- email.meme.text: https://docs.python.org/3.7/library/email.mime.html#email.mime.text.MIMEText
- email.meme.image: https://docs.python.org/3.7/library/email.mime.html#email.mime.image.MIMEImage
- time.sleep: https://docs.python.org/3.7/library/time.html#time.sleep
- random.randint: https://docs.python.org/3/library/random.html#random.randint
- os.listdir: https://docs.python.org/3/library/os.html#os.listdir
- email examples: https://docs.python.org/3.7/library/email.examples.html

"""
# import project libraries
import os # used to locate the image files
import random # used to generate a random number for pulling an image from the list
import time # used to create a delay between sending emails
import smtplib as smtp # used for actually sending the email

## used for building the email message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


# setup server authentication variables
user = 'user@gmail.com'
password = 'pas$w0rd'
fr_address = 'me@gmail.com'
to_address = 'you1@gmail.com, you2@gmail.com, you3@gmail.com, you4@gmail.com'
smtp_host = 'smtp.gmail.com'

# setup email variables
subject = 'Get back to WORK!!'
msg_text = 'what do you think you\'re doing?'
msg_count = 20


# create email message

## get a list of all messages in the image directory
memes = os.listdir('img')

## create the multipart email message and add from ,to, and subject headers
msg = MIMEMultipart()
msg['From'] = fr_address
msg['To'] = to_address
msg['Subject'] = subject

## create an html message with a reference to the image source attribute referenced below
body = MIMEText(f'<b><i>{msg_text}</b></i><br><br><img src="cid:myimage"/>','html')

## open a connection to the email server
server = smtp.SMTP(host=smtp_host, port=587)
server.starttls()
server.login(user=user, password=password)

## create and send the message
for i in range(msg_count):
    
    # open a random image from the image directory
    rnd_image = memes[random.randint(0,len(memes)-1)]
    with open(f'img/{rnd_image}','rb') as f:
        msg_image = MIMEImage(f.read())

    # create the message content ID referenced above
    msg_image.add_header('Content-ID','myimage')

    # set the message payload
    '''
    We can't use the MIMEText.attach() method here otherwise it will add additional parts
    each consecutive email. Using the MIMEText.set_payload() method basically resets this 
    each time
    '''
    msg.set_payload([body, msg_image])

    # open the email server and send the message
    server.send_message(msg)
    
    # delay the next message by 60 seconds... you can change this if you want
    time.sleep(60)

server.close()