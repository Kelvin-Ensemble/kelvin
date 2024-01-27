
from django.urls import path, re_path

from . import views
from . import ticketRouting
from django.contrib import admin

import os,sys
sys.path.insert(1, os.path.dirname(os.path.realpath(__file__)) + '/')

urlpatterns = [
    #home
    path('', views.home, name='home'),

    #concerts
    path('concerts', views.concerts, name='concerts'),

    #payments
    path('payment_successful', ticketRouting.payment_successful, name='payment_successful'),
    # url(r'^payment_cancelled$', ticketRouting.payment_cancelled, name='payment_cancelled'),
    path('stripe_webhook', ticketRouting.stripe_webhook, name='stripe_webhook'),
    path('payment', ticketRouting.payment_page, name='payment'),

    #players
    path('info', views.info, name='info'),
    path('calendar', views.calendar, name='calendar'),
    path('join', views.join, name='join'),
    path('composition', views.composition, name='composition'),
    # Comment out lines below to deactivate URLs when auditions are not taking place.
    # url(r'^string-auditions$', views.stringAuditions, name='string-auditions'),
    # url(r'^bwp-auditions$', views.bwpAuditions, name='bwp-auditions'),

    #about
    path('past-concerts', views.pastConcerts, name='past-concerts'),
    path('history', views.history, name='history'),
    path('gallery', views.gallery, name='gallery'),
    path('videos', views.videos, name='videos'),
    path('committee', views.committee, name='committee'),
    path('associates', views.associates, name='associates'),
    path('conductor', views.conductor, name='conductor'),
    
    #contact
    path('contact', views.contact, name='contact'),
    path('mailing-list', views.mailingList, name='mailing-list'),
    path('support', views.support, name='support'),

    #404
    re_path(r'^', views.notFound, name='404'),

        
]

# import timedFunctions
#
# timedFunctions.beginTimed()