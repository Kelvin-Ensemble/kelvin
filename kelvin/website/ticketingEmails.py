from django.conf import settings

import webbrowser
import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import re

import ssl
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from email.mime.image import MIMEImage


def createEmail(customerDetails, items, template):
    with open(template, encoding="utf-8") as f:
        html = f.read()

    rendered = render_to_string(
        template, {"customerDetails": customerDetails, "items": items}
    )

    return rendered


def sendEmail(customerDetails, items, template, programme):
    sender_password = settings.TICKETS_PASSWORD
    sender_address = "tickets@kelvin-ensemble.co.uk"

    customerName = customerDetails["name"]
    customerEmail = customerDetails["email"]

    templateDir = os.getcwd() + "\\kelvin\\kelvin\\website\\templates\\ticketing\\"

    stringMsg = "This is an automated email, please do not reply to this email. Please email: webmaster@kelvin-ensemble.co.uk if there are any problems. \n \nIf you are seeing this message, your browser/device does not support viewing this email. \n\nDear " + customerName + "\n\nWe can confirm you have bought the following tickets:"

    # create written message
    for item in items:
        stringMsg = stringMsg +  "\n\n" + str(item["qty"]) + " " +  str(item["label"]) + " ticket(s)"


    stringMsg = stringMsg + "\n\nWe will have a list of names matching the names given. The name on this purchase is: " + customerName +  "\n\nPlease be ready to provide this information on arrival."

    stringMsg = stringMsg + "\n\nLocation: " + items[0]["concertLoc"]
    stringMsg = stringMsg + "\n\nDate: " + items[0]["concertDate"].strftime("%m/%d/%Y, %H:%M:%S")

    stringMsg = stringMsg + "\n\nPlease use the following link to view the original email in your web browser: \nhttps://www.kelvin-ensemble.co.uk/email_viewer"

    # html = createEmail(customerDetails, items, template)
    html = render_to_string(
        template, {"customerDetails": customerDetails, "items": items}
    )
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_address
    msg["To"] = customerEmail
    msg["Subject"] = "Concert Ticket(s) - Kelvin Ensemble"
    part1 = MIMEText(
        stringMsg,
        "plain",
    )
    part2 = MIMEText(html, "html", "utf-8")

    with open(templateDir + programme, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
    attach.add_header("Content-Disposition", "attachment", filename=str(programme))
    msg.attach(attach)
    # pdf = createPDFofEmail(html)
    # attach = MIMEApplication(pdf, _subtype="pdf")
    # attach.add_header('Content-Disposition', 'attachment', filename="email_content")
    # msg.attach(attach)

    fp = open(os.path.realpath(templateDir + "KELogoLong.jpg"), "rb")
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header("Content-ID", "<kelLogo1>")
    msg.attach(msgImage)

    msg.attach(part1)
    msg.attach(part2)

    email_string = msg.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_address, sender_password)
        server.sendmail(msg["From"], msg["To"], email_string)

    print("Email sent!")
