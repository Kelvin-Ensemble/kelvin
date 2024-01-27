from django.contrib import admin
from .models import Ticket
from .models import Concert
from .models import TicketType
from import_export.admin import ExportActionMixin

# Register your models here.


class ticketsAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["name", "email", "transaction_ID", "validity"]
    list_filter = ["for_concert", "ticket_type", "validity"]
    search_fields = ["name", "email", "transaction_ID"]
    search_help_text = "Search for matching name, email or transaction ID."


class ticketTypesAdmin(admin.ModelAdmin):
    readonly_fields = ["Quantity_available", "Linked_sold"]
    filter_horizontal = ["Linked_Tickets"]


admin.site.site_header = "Kelvin Ensemble Web Admin"
admin.site.site_title = "Kelvin Ensemble Web Admin"

admin.site.register(Concert)
admin.site.register(TicketType, ticketTypesAdmin)
admin.site.register(Ticket, ticketsAdmin)
