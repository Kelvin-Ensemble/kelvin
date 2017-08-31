from django.shortcuts import render

def home(request):
    print ("Home")
    return render(request, 'website/home.html')

def concerts(request):
    print ("Concerts")
    return render(request, 'website/concerts.html')

