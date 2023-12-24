import os,sys
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
import datetime
from django.views.decorators.csrf import csrf_exempt

sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/')
from ticketRouting import payment_page


#home
def home(request):
    return render(request, 'website/home.html')


@csrf_exempt
def concerts(request):
    if request.method == 'POST':
        print("redirecting to payment")
        redirect('payment')
    else:
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

