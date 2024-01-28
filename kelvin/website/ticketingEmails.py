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

    # with open("output/"+vars["name"]+ ".html", "w", encoding="utf-8") as text_file:
    #     text_file.write(output)

    # webbrowser.open("file://" + os.path.realpath("output/"+vars["name"]+ ".html"))

    return rendered


def sendEmail(customerDetails, items, template, programme):
    sender_password = settings.TICKETS_PASSWORD
    sender_address = "tickets@kelvin-ensemble.co.uk"

    customerName = customerDetails["name"]
    customerEmail = customerDetails["email"]

    templateDir = os.getcwd() + "\\website\\templates\\ticketing\\"

    # html = createEmail(customerDetails, items, template)
    html = render_to_string(
        template, {"customerDetails": customerDetails, "items": items}
    )
    msg = MIMEMultipart("alternative")
    msg["From"] = sender_address
    msg["To"] = customerEmail
    msg["Subject"] = "Concert Ticket(s) - Kelvin Ensemble"
    part1 = MIMEText(
        "This is an automated email, please do not reply to this email. Please email: webmaster@kelvin-ensemble.co.uk if there are any problems. \n If you are seeing this message, your browser/device does not support viewing this email. Please see the 'email_content' PDF attached for the contents of this email.",
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
