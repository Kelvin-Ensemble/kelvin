import datetime
import os
from django.conf import settings
import stripe
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from ticketingEmails import sendEmail
from website.models import Concert, TicketType, Ticket

ticketGenDir = (os.path.dirname(os.path.realpath(__file__))) + "/"
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


def updateQuantities():  # Function to check whether the variables relevant in stock counting exist or not
    print("Updating Quantites")
    for ticket in TicketType.objects.all():
        linked_sold = 0

        for linked in ticket.Linked_Tickets.all():
            print("Linked object as sold", linked.Quantity_sold, "numebr of tix")
            linked_sold += linked.Quantity_sold

        qtyAvail = ticket.Total_ticket_count - linked_sold - ticket.Quantity_sold

        if (ticket.Linked_sold != linked_sold) or (ticket.Quantity_available != qtyAvail):
            ticket.Linked_sold = linked_sold
            ticket.Quantity_available = qtyAvail
            ticket.save()


def processWebhookRequest(request):
    print("Webhook triggerrededededed")
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    endpoint_secret = os.environ["STRIPE_ENDPOINT_KEY"]
    print("is this still working?")

    payload = request.body
    print("yes it is.")

    try:
        event = json.loads(payload)
        print(event)

    except:
        print("⚠️  Webhook error while parsing basic request. \n")
    if endpoint_secret:
        sig_header = request.headers["stripe-signature"]
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except stripe.error.SignatureVerificationError as e:
            print("⚠️  Webhook signature verification failed." + str(e))
            return json.dumps(success=False)
    # print(payload['type'])
    # print(payload['request']['type'])
    print("checking for event type")



    if event and event["type"] == "checkout.session.completed":

        print("Order Success")
        orderDetails = event["data"]  # contains a stripe.PaymentIntent
        paymentID = event["data"]["object"]["id"]
        line_items = stripe.checkout.Session.list_line_items(paymentID)["data"]
        customer_info = event["data"]["object"]["customer_details"]
        customer_info["name"] = event["data"]["object"]["custom_fields"][0]["text"][
            "value"
        ]

        if Ticket.objects.filter(transaction_ID = event["data"]["object"]["id"]).exists():
            print("ALREADY PROCESSED THIS TRANSACTION")
            return True
        else:
            # print(event)
            # print(orderDetails)
            # print(paymentID)
            # print(line_items)
            # print(type(line_items))
            print(event["data"])
            print(customer_info)

            items = []

            print("Itemised line items")
            for ticket in TicketType.objects.all():
                print("Looking for ticket")
                for item in line_items:
                    print("Finding item id in ticket")
                    if item["price"]["id"] == ticket.Price_ID:
                        items.append(
                            {
                                "price_id": item["price"]["id"],
                                "qty": item["quantity"],
                                "label": ticket.ticket_label,
                                "concertDate": ticket.for_concert.Concert_Date,
                                "concertLoc": ticket.for_concert.Concert_location,
                            }
                        )
                        print("Found correct id")
                        if item["quantity"] > ticket.Quantity_available:
                            print("OVERSELLING!!!!!")
                            # return False

            print("checkout accepted")

            print(items)
            for item in items:
                ticketType = None
                for ticket in TicketType.objects.all():
                    if item["price_id"] == ticket.Price_ID:
                        print("Found ticket and adding concert to details")
                        ticketType = ticket
                        ticket.Quantity_sold += item["qty"]
                        ticket.save()
                        customer_info["concertDate"] = ticket.for_concert.Concert_Date
                        customer_info["concertLoc"] = ticket.for_concert.Concert_location
                        break

                for i in range(int(item["qty"])):
                    newEntry = Ticket(
                        name=customer_info["name"],
                        email=customer_info["email"],
                        transaction_ID=event["data"]["object"]["id"],
                        for_concert=ticketType.for_concert,
                        ticket_type=ticketType,
                        validity=True,
                        change_log="[{}] - Payment Accepted".format(datetime.datetime.utcnow()),
                    )
                    newEntry.save()
                    print("Saved ticket")

            # print(customer_info)

            templateDir = os.getcwd() + "/kelvin/kelvin/website/templates/ticketing/"

            sendEmail(
                customer_info, items, "ticketing/template.html", "Concert_Programme.pdf"
            )
            # sendConfirmation(items, customer_info, paymentID)
    else:
        # Unexpected event type
        print("Unhandled event type {}".format(event["type"]))

    return True
