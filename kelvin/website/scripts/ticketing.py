import os
from django.conf import settings
import ssl
import smtplib
import stripe

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders
from email.mime.image import MIMEImage

ticketGenDir = (os.path.dirname(os.path.realpath(__file__)))  + '/'


stripe.api_key = "sk_test_51MlGRwDysBLU7VPvb6H1HJphyfTVkjEpOxb6mNuLv0Sn1qLFCyeuO7GUOmMN1lwSTNWlYDENvWii0e2uKwRIu8MA00lgj9fiR8"

def sendConfirmation(cartInfo, customerDetails, pid):
    html = open(ticketGenDir + "confirmation_template.html")
    sender_password = settings.TICKETS_PASSWORD
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

def updateQty():
    for j in range(len(settings.CONCERT_LIST)):
        print(settings.CONCERT_LIST[j])
        for i in range(len(settings.CONCERT_LIST[j]["tickets"])):
            if not hasattr(settings.CONCERT_LIST[j]["tickets"][i], "prodID"):
                print("No prodID attribute")
                price_info = stripe.Price.retrieve(settings.CONCERT_LIST[j]["tickets"][i]["ticketID"])
                productID = price_info["product"]
                print(productID)
                settings.CONCERT_LIST[j]["tickets"][i]["prodID"] = productID

            if not hasattr(settings.CONCERT_LIST[j]["tickets"][i], "qtyAvail"):
                settings.CONCERT_LIST[j]["tickets"][i]["qtyAvail"] = 0
            if not hasattr(settings.CONCERT_LIST[j]["tickets"][i], "qtyAvail"):
                settings.CONCERT_LIST[j]["tickets"][i]["qtyAvailRange"] = ""

            settings.CONCERT_LIST[j]["tickets"][i]["qtyAvailRange"] = ""


            product_info = stripe.Product.retrieve(settings.CONCERT_LIST[j]["tickets"][i]["prodID"])


            if hasattr(product_info["metadata"], "max_sales") and hasattr(product_info["metadata"], "total_sales"):
                availability = int(product_info["metadata"]["max_sales"]) - int(product_info["metadata"]["total_sales"])
                print(availability)
                settings.CONCERT_LIST[j]["tickets"][i]["qtyAvail"] = availability
                for k in range(1,int(availability) + 1):
                    settings.CONCERT_LIST[j]["tickets"][i]["qtyAvailRange"] += str(k)
            else:
                print("ERROR NO SALES INFO AVAILABLE")
                settings.CONCERT_LIST[j]["tickets"][i]["qtyAvail"] = "ERROR NO SALES METADATA"





