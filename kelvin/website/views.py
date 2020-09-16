
from django.http import HttpResponse
from django.shortcuts import render

#home
def home(request):
    return render(request, 'website/home.html')


#concerts
def concerts(request):
    return render(request, 'website/concerts.html')


#players
def info(request):
    return render(request, 'website/players/info.html')

def calendar(request):
    return render(request, 'website/players/calendar.html')

def join(request):
    return render(request, 'website/players/join.html')

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
