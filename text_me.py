import time
import smtplib
import RPi.GPIO as GPIO

TO= "2488778790@vtext.com" #all of the credentials
GMAIL_USER="roufeshound@gmail.com"
PASS= 'caesiopkckblufyd'

SUBJECT = 'Alert!'
TEXT = 'Your Raspberry Pi detected an intruder!'



def send_mail(): #the texting portion
    print("Sending text")
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(GMAIL_USER,PASS)
    header = 'To: ' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject: ' + SUBJECT + '\n'
    print(header)
    msg = header + '\n' + TEXT + '\n\n'
    server.sendmail(GMAIL_USER,TO,msg)
    server.quit()
    time.sleep(1)
    print("Text sent")

send_mail()

