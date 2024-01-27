from django.contrib import admin
from .models import Ticket
from .models import Concert
from .models import TicketType

# Register your models here.

admin.site.site_header = "Kelvin Ensemble Web Admin"
admin.site.site_title = "Kelvin Ensemble Web Admin"

admin.site.register(Concert)
admin.site.register(TicketType)
