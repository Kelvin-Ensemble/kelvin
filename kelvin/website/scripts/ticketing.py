import kelvin_secrets
import os
from django.conf import settings
import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from email.mime.image import MIMEImage

ticketGenDir = (os.path.dirname(os.path.realpath(__file__)))  + '/'
def sendConfirmation(cartInfo, customerDetails, pid):
    html = open(ticketGenDir + "confirmation_template.html")
    sender_password = kelvin_secrets.email_password
    sender_address = 'tickets@kelvin-ensemble.co.uk'

    customerName = customerDetails["name"]
    customerEmail = customerDetails["email"]

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_address
    msg['To'] = customerEmail
    msg['Subject'] = "Tickets for " + settings.CONCERT_NAME + " - Kelvin Ensemble"
    msg.attach(MIMEText(html.read().format(customerName, settings.CONCERT_NAME, pid), 'html'))

    fp = open(ticketGenDir + 'KELogoLong.jpg', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header('Content-ID', '<kelLogo1>')
    msg.attach(msgImage)

    email_string = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_address, sender_password)
        server.sendmail(msg['From'], msg['To'], email_string)