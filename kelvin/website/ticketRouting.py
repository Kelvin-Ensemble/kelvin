import stripe
import json
import os,sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_page(request):
    try:
        session = stripe.checkout.Session.create(
            ui_mode='embedded',
            line_items=[
                {
                    # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                    'price': request.POST.__getitem__('ticketID'),
                    'quantity': request.POST.__getitem__('ticketQty'),
                },
            ],
            mode='payment',
            return_url='http://127.0.0.1:8000' + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
        )
    except Exception as e:
        print(str(e))

    return render(request, 'website/payment.html', {'clientSecret': session.client_secret, 'stripePKey': settings.STRIPE_PUBLIC_SECRET})

def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    return render(request, 'website/payment_successful.html', {'customer':customer})

@csrf_exempt
def stripe_webhook(request):
    print("Webhook triggerrededededed")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    print("is this still working?")

    payload = request.body
    print("yes it is.")

    try:
        event = json.loads(payload)
        print(event)

    except:
        print('⚠️  Webhook error while parsing basic request. \n')
    if endpoint_secret:
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return json.dumps(success=False)
    # print(payload['type'])
    # print(payload['request']['type'])
    print("checking for event type")

    if event and event['type'] == 'checkout.session.completed':
        print("Order Success")
        orderDetails = event['data']  # contains a stripe.PaymentIntent
        paymentID = event['data']["object"]["id"]
        line_items = stripe.checkout.Session.list_line_items(paymentID)['data']
        customer_info = event['data']["object"]["customer_details"]
        # print(event)
        # print(orderDetails)
        # print(paymentID)
        # print(line_items)
        print(customer_info)
        ticketing.sendConfirmation(line_items,customer_info, paymentID)
    else:
        # Unexpected event type
        print('Unhandled event type {}'.format(event['type']))

    return HttpResponse(200)
