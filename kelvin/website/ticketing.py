import os
from django.conf import settings
import stripe
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect

ticketGenDir = (os.path.dirname(os.path.realpath(__file__))) + "/"
stripe.api_key = settings.STRIPE_SECRET_KEY


def checkQtyVars():  # Function to check whether the variables relevant in stock counting exist or not
    for j in range(len(settings.CONCERT_LIST)):
        for i, ticket in enumerate(settings.CONCERT_LIST[j]["tickets"]):
            if not ("prodID" in ticket):  # If there is no product ID property, add that
                print("No prodID attribute", ticket)
                price_info = stripe.Price.retrieve(
                    ticket["ticketID"]
                )  # Retrieve product ID
                ticket["prodID"] = price_info["product"]

            if not ("qtyAvail" in ticket):
                ticket["qtyAvail"] = 0
            if not ("dSold" in ticket):
                ticket["dSold"] = 0
            if not ("maxAvail" in ticket):
                ticket["maxAvail"] = 0
            if not ("totalSold" in ticket):
                ticket["totalSold"] = 0
            if not ("qtyAvailRange" in ticket):
                ticket["qtyAvailRange"] = ""

        for i, ticket in enumerate(settings.CONCERT_LIST[j]["tickets"]):
            if not ("linkedProducts" in ticket):
                print("Finding matches", ticket)
                ticket["linkedProducts"] = []
                for k, l in enumerate(settings.CONCERT_LIST[j]["tickets"]):
                    if l["prodID"] == ticket["prodID"] and i != k:
                        print("Found a match!", i, k)
                        ticket["linkedProducts"].append(k)

    ticket["qtyAvailRange"] = ""


def publishSoldData(ticket):
    stripe.Product.modify(
        ticket["prodID"],
        metadata={"total_sales": ticket["totalSold"] + ticket["qtySoldSinceRefresh"]},
    )


def updateQty():  # Function that updates the quantities remaining of each ticket
    checkQtyVars()
    for j in range(len(settings.CONCERT_LIST)):
        for i, v in enumerate(settings.CONCERT_LIST[j]["tickets"]):
            product_info = stripe.Product.retrieve(v["prodID"])
            print(v)
            if ("max_sales" in product_info["metadata"]) and (
                "total_sales" in product_info["metadata"]
            ):  # If the product has correct metadata
                totalSales = int(product_info["metadata"]["total_sales"])
                maxSales = int(product_info["metadata"]["max_sales"])
                availability = maxSales - totalSales
                print(availability)
                v["qtyAvail"] = availability
                v["totalSold"] = totalSales
                v["maxAvail"] = maxSales
                for k in range(
                    1, int(availability) + 1
                ):  # Creates a string of numbers for use in the dropdowns ("123" for 3, "1234567" for 7)
                    v["qtyAvailRange"] += str(k)

                if (
                    v["dSold"] != 0
                ):  # If there is a difference in sold (i.e. there has been a change)
                    publishSoldData(v)

            else:
                print("ERROR NO SALES INFO AVAILABLE")
                v["qtyAvail"] = "ERROR NO SALES METADATA"


def holdPurchase():
    # Function to hold tickets whilst a transaction is taking place (will just add to the dSold (assume it has been sold))
    pass


def expirePurchase():
    # Function to expire a purchase and "unreserve" the persons ticket if they have taken too long, or the browser window expires. (lowers dSold)
    pass
