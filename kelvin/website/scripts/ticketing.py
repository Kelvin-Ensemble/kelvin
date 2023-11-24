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

def checkQtyVars(ticket): # Function to check whether the variables relevant in stock counting exist or not
    if not ("prodID" in ticket): # If there is no product ID property, add that
        print("No prodID attribute", ticket)
        price_info = stripe.Price.retrieve(ticket["ticketID"]) # Retrieve product ID
        ticket["prodID"] = price_info["product"]

    if not ("qtyAvail" in ticket):
        ticket["qtyAvail"] = 0
    if not ("dSold" in ticket):
        ticket["dSold"] = 0
    if not ("maxAvail" in ticket):
        ticket["maxAvail"] = 0
    if not ("totalSold" in ticket):
        ticket["totalSold"] = 0

    ticket["qtyAvailRange"] = ""

def publishSoldData(ticket):
    stripe.Product.modify(
        ticket["prodID"],
        metadata={"total_sales": ticket["totalSold"] + ticket["qtySoldSinceRefresh"]},
    )


def updateQty(): # Function that updates the quantities remaining of each ticket
    for j in range(len(settings.CONCERT_LIST)):
        for i,v in enumerate(settings.CONCERT_LIST[j]["tickets"]):
            checkQtyVars(v)
            product_info = stripe.Product.retrieve(v["prodID"])

            if ("max_sales" in product_info["metadata"]) and ("total_sales" in product_info["metadata"]): # If the product has correct metadata
                totalSales = int(product_info["metadata"]["total_sales"])
                maxSales = int(product_info["metadata"]["max_sales"])
                availability = maxSales - totalSales
                print(availability)
                v["qtyAvail"] = availability
                v["totalSold"] = totalSales
                v["maxAvail"] = maxSales
                for k in range(1,int(availability) + 1): # Creates a string of numbers for use in the dropdowns ("123" for 3, "1234567" for 7)
                    v["qtyAvailRange"] += str(k)

                if (v["dSold"] != 0): # If there is a difference in sold (i.e. there has been a change)
                    publishSoldData(v)

            else:
                print("ERROR NO SALES INFO AVAILABLE")
                v["qtyAvail"] = "ERROR NO SALES METADATA"





