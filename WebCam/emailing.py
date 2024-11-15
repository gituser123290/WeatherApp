
import smtplib
import imghdr
from email.message import EmailMessage

SENDER_PASSWORD="tjuj lvro aswp gtdq"
SENDER_EMAIL="naurangilal9675329115@gmail.com"

RECIEVER_EMAIL='naurangilal15072002@gmail.com'

def send_mail(image_path):
    email_message=EmailMessage()
    email_message["Subject"]="New customer showed up"
    email_message.set_content("Hey we just saw a new customer!")
    
    with open(image_path,'rb') as file:
        content=file.read()
    
    email_message.add_attachment(content,maintype='image',subtype=imghdr.what(None,content))
    
    gmail=smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER_EMAIL,SENDER_PASSWORD)
    gmail.sendmail(SENDER_EMAIL,RECIEVER_EMAIL,email_message.as_string())
    gmail.quit()
    
    
if __name__=="__main__":
    send_mail()