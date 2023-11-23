
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import datetime
import stripe
import json
import os,sys

from django.views.decorators.csrf import csrf_exempt



#home
def home(request):
    return render(request, 'website/home.html')


@csrf_exempt
def concerts(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        print(request.POST)
        print(request.POST['concessionTicketQty'])
        print(request.POST.get('concessionTicketID'))
        basket = []

        if int(request.POST.get('standardTicketQty')) > 0:
            basket.append({
                'price': request.POST.get('standardTicketID'),
                'quantity': request.POST['standardTicketQty'],
            })

        if int(request.POST.get('concessionTicketQty')) > 0:
            basket.append({
                'price': request.POST.get('concessionTicketID'),
                'quantity': request.POST['concessionTicketQty'],
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=basket,
            mode='payment',
            customer_creation='always',
            success_url=settings.REDIRECT_DOMAIN + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=settings.REDIRECT_DOMAIN + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'website/concerts.html')



#players
def info(request):
    return render(request, 'website/players/info.html')

def calendar(request):
    return render(request, 'website/players/calendar.html')

def join(request):
    return render(request, 'website/players/join.html')

def composition(request):
    date = datetime.datetime.utcnow()

    competitionPlanned = False

    # Competition Opening day info
    competitionOpenDay = 16
    competitionOpenMonth = 6
    competitionOpenYear = 2023
    competitionOpenHour = 11
    competitionOpenMin = 0


    # Check if its day of competition opening
    if not competitionPlanned:
        return render(request, 'website/players/compositionNotPlanned.html')
    elif date.day == competitionOpenDay and date.month == competitionOpenMonth and date.year == competitionOpenYear:
        # If it is the day, is it before or after the hour it opens?
        if date.hour >= competitionOpenHour:
            # Is it before or after the minute it opens?
            if date.minute >= competitionOpenMin:
                return render(request, 'website/players/composition.html')
            else:
                return render(request, 'website/players/compositionnotopen.html')
        else:
            return render(request, 'website/players/compositionnotopen.html')
    # If the year the competition opens
    elif date.year == competitionOpenYear:
        # If over a month after the competition opens or if it is in the same month but after the day
        if date.month > competitionOpenMonth or (date.month == competitionOpenMonth and date.day > competitionOpenDay):
            return render(request, 'website/players/composition.html')
    elif date.year > competitionOpenYear:
        return render(request, 'website/players/composition.html')
    elif competitionPlanned:
        return render(request, 'website/players/compositionnotopen.html')

    return render(request, 'website/players/compositionNotPlanned.html')



# def stringAuditions(request):
#   return render(request, 'website/players/string-auditions.html')

# def bwpAuditions(request):
#    return render(request, 'website/players/bwp-auditions.html')


#about
def pastConcerts(request):
    return render(request, 'website/about/past-concerts.html')

def history(request):
    return render(request, 'website/about/history.html')

def gallery(request):
    return render(request, 'website/about/gallery.html')

def videos(request):
    return render(request, 'website/about/videos.html')

def committee(request):
    return render(request, 'website/about/committee.html')

def associates(request):
    return render(request, 'website/about/associates.html')

def conductor(request):
    return render(request, 'website/about/conductor.html')


#contact
def contact(request):
    return render(request, 'website/contact/contact.html')

def mailingList(request):
    return render(request, 'website/contact/mailing-list.html')

def support(request):
    return render(request, 'website/contact/support.html')


#404
def notFound(request):
    return render(request, 'website/404.html')


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
