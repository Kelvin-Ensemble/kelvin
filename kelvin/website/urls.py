
from django.conf.urls import url

from . import views

urlpatterns = [
    #home
    url(r'^$', views.home, name='home'),

    #concerts
    url(r'^concerts$', views.concerts, name='concerts'),

    #players
    url(r'^info$', views.info, name='info'),
    url(r'^join$', views.join, name='join'),
    url(r'^calendar$', views.calendar, name='calendar'),

    #about
    url(r'^past-concerts$', views.pastConcerts, name='past-concerts'),
    url(r'^history$', views.history, name='history'),
    url(r'^gallery$', views.gallery, name='gallery'),
    url(r'^videos$', views.videos, name='videos'),
    url(r'^committee$', views.committee, name='committee'),
    url(r'^bios$', views.bios, name='bios'),
    url(r'^conductor$', views.conductor, name='conductor'),
    
    #contact
    url(r'^contact$', views.contact, name='contact'),
    url(r'^mailing-list$', views.mailingList, name='mailing-list'),
    url(r'^support$', views.support, name='support'),

    #404
    url(r'^', views.notFound, name='404'),
        
]
