
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import datetime
import stripe


#home
def home(request):
    return render(request, 'website/home.html')


#concerts
def concerts(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
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


def payment_successful(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    customer = stripe.Customer.retrieve(session.customer)
    return render(request, 'website/payment_successful.html', {'customer':customer})


#players
def info(request):
    return render(request, 'website/players/info.html')

def calendar(request):
    return render(request, 'website/players/calendar.html')

def join(request):
    return render(request, 'website/players/join.html')

def composition(request):
    date = datetime.datetime.utcnow()

    competitionPlanned = True

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
