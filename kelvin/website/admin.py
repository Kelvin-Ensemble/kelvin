from django.contrib import admin
from .models import Ticket
from .models import Concert
from .models import TicketType
from import_export.admin import ExportMixin
from import_export.admin import ImportExportModelAdmin
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget

# Register your models here.

class ticketResource(resources.ModelResource):
    def get_export_headers(self):
        headers = super().get_export_headers()
        for i, h in enumerate(headers):
            if h == 'name': headers[i] = "Name"
            if h == 'email': headers[i] = "Email"
            if h == 'for_concert__Concert_Nickname': headers[i] = "Concert"
            if h == 'ticket_type__ticket_label': headers[i] = "Ticket Type"
            if h == 'change_log': headers[i] = "Changelog"
        return headers
    class Meta:
        model = Ticket
        fields = ('name', 'email', 'for_concert__Concert_Nickname', 'ticket_type__ticket_label', 'validity', 'change_log')
        export_order = ['name', 'email', 'for_concert__Concert_Nickname', 'ticket_type__ticket_label', 'validity', 'change_log']

@admin.register(Ticket)
class ticketAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ticketResource
    list_display = ["name", "email", "transaction_ID", "ticket_type", "validity"]
    list_filter = ["for_concert", "ticket_type", "validity"]
    search_fields = ["name", "email", "transaction_ID"]
    search_help_text = "Search for matching name, email or transaction ID."

@admin.register(TicketType)
class ticketTypesAdmin(admin.ModelAdmin):
    readonly_fields = ["Quantity_available", "Linked_sold", "Tickets_in_database"]
    list_display = ["ticket_label", "for_concert", "Quantity_available"]
    filter_horizontal = ["Linked_Tickets"]


admin.site.site_header = "Kelvin Ensemble Web Admin"
admin.site.site_title = "Kelvin Ensemble Web Admin"

admin.site.register(Concert)
# admin.site.register(TicketType, ticketTypesAdmin)
# admin.site.register(Ticket, ticketsAdmin)
