
from django.conf.urls import url

from . import views

urlpatterns = [
    #home
    url(r'^$', views.home, name='home'),

    #concerts
    url(r'^concerts$', views.concerts, name='concerts'),

    #payments
    url(r'^payment_successful$', views.payment_successful, name='payment_successful'),

    #players
    url(r'^info$', views.info, name='info'),
    url(r'^calendar$', views.calendar, name='calendar'),
    url(r'^join$', views.join, name='join'),
    url(r'^composition$', views.composition, name='composition'),
    # Comment out lines below to deactivate URLs when auditions are not taking place.
    # url(r'^string-auditions$', views.stringAuditions, name='string-auditions'),
    # url(r'^bwp-auditions$', views.bwpAuditions, name='bwp-auditions'),

    #about
    url(r'^past-concerts$', views.pastConcerts, name='past-concerts'),
    url(r'^history$', views.history, name='history'),
    url(r'^gallery$', views.gallery, name='gallery'),
    url(r'^videos$', views.videos, name='videos'),
    url(r'^committee$', views.committee, name='committee'),
    url(r'^associates$', views.associates, name='associates'),
    url(r'^conductor$', views.conductor, name='conductor'),
    
    #contact
    url(r'^contact$', views.contact, name='contact'),
    url(r'^mailing-list$', views.mailingList, name='mailing-list'),
    url(r'^support$', views.support, name='support'),

    #404
    url(r'^', views.notFound, name='404'),
        
]
