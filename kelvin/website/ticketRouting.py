import stripe
import json
import os, sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from ticketing import processWebhookRequest
from website.models import Concert, TicketType


def viewEmail(request):
    return render(request, "ticketing/empty_template.html")

@csrf_exempt
def payment_page(request):
    if request.method == "GET":
        try:
            print(request)
            cart = json.loads(request.GET.get("cart"))
            # print(json.loads(cart))

            items = []

            for item in cart:
                print("Appending: " + item["ticketID"])
                items.append(
                    {
                        "price": item["ticketID"],
                        "quantity": item["qtySelected"],
                    }
                )

                for ticket in TicketType.objects.all():
                    if item["ticketID"] == ticket.Price_ID:
                        if item["qtySelected"] > ticket.Quantity_available:
                            return HttpResponse(status=400)

            print(items)

            session = stripe.checkout.Session.create(
                ui_mode="embedded",
                line_items=items,
                mode="payment",
                return_url="https://www.kelvin-ensemble.co.uk"
                + "/payment_successful?session_id={CHECKOUT_SESSION_ID}",
                custom_fields=[
                    {
                        "key": "tixName",
                        "label": {"type": "custom", "custom": "Name on ticket"},
                        "type": "text",
                    }
                ],
            )

            print(session)

            response = render(
                request,
                "website/payment.html",
                {
                    "clientSecret": session.client_secret,
                    "stripePKey": os.environ["STRIPE_PUBLIC_SECRET"],
                },
            )

            print(response)

            return render(
                request,
                "website/payment.html",
                {
                    "clientSecret": session.client_secret,
                    "stripePKey": os.environ["STRIPE_PUBLIC_SECRET"],
                },
            )

        except Exception as e:
            print(str(e))
            print("ERROR OCCURED SEE ABOVE FOR TRACE")

    return render(request, "website/404.html")


def payment_successful(request):
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    checkout_session_id = request.GET.get("session_id", None)
    print(checkout_session_id)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    print(session)
    customer_details = {
        "name": session["custom_fields"][0]["text"]["value"],
        "email": session["customer_details"]["email"],
    }
    return render(
        request, "website/payment_successful.html", {"customer": customer_details}
    )

def payment_cancelled(request):
    return render(request, "website/payment_failed.html")

@csrf_exempt
def stripe_webhook(request):
    result = processWebhookRequest(request)
    print(result)
    if result == True:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
