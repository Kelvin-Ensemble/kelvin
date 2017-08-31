
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

def join(request):
    return render(request, 'website/players/join.html')

def calendar(request):
    return render(request, 'website/players/calendar.html')


#about
def pastConcerts(request):
    return render(request, 'website/about/past-concerts.html')

def history(request):
    return render(request, 'website/about/history.html')

def gallery(request):
    return render(request, 'website/about/gallery.html')


#contact
def contact(request):
    return render(request, 'website/contact.html')

#support
def support(request):
    return render(request, 'website/support.html')

#404
def notFound(request):
    return render(request, 'website/404.html')