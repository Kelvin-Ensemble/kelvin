from django.db import models
from datetime import datetime


# Create your models here.
class Concert(models.Model):
    status_choices = (
        ("OV", "Over"),
        ("FS", "For Sale"),
        ("UC", "Upcoming"),
        ("SO", "Sold Out"),
        ("NY", "Not Yet"),
    )
    Concert_Nickname = models.CharField(
        max_length=15,
        help_text="This is just a nickname for this concert to make it easier for you to distinguish in the admin page.",
        null=False,
        blank=False,
        default="Concert",
    )
    Concert_Status = models.CharField(max_length=2, choices=status_choices)
    Concert_Date = models.DateTimeField(default=datetime.now, blank=True)
    Concert_location = models.TextField(default="")

    def __str__(self):
        return self.Concert_Nickname


class TicketType(models.Model):
    ticket_label = models.CharField(
        max_length=40,
        help_text="This will be the ticket name shown to the audience (i.e. 'Standard Seating' or 'Concession Seating' or 'Restricted View')",
    )
    for_concert = models.ForeignKey(
        Concert,
        help_text="Please select the matching concert here. Make sure this is selected or the ticket will not show.",
        on_delete=models.CASCADE,
        default=None,
        null=True,
    )
    Price_ID = models.CharField(
        max_length=40,
        help_text="This will be the price ID supplied by STRIPE which you can obtain via the treasurer. Refer to the webmaster bible's payments section for more information",
    )
    Linked_Tickets = models.ManyToManyField(
        "TicketType",
        blank=True,
        help_text="This should auto-populate when saving as long as the STRIPE products and prices are set up correctly. If this does not happen it may be done manually here. However it is not recommended.",
    )
    display_ticket = models.BooleanField(
        default=False,
        help_text="When ticked, this will show as a purchasable ticket. This should only be false for complimentary tickets.",
    )
    # Product_ID = models.CharField(max_length=40, blank=True, null=True, default="",
    #                               help_text="This data is automatically taken from STRIPE")

    Total_ticket_count = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="This data is automatically taken from STRIPE metadata",
    )

    # ReadOnly Values
    Quantity_sold = models.IntegerField(
        blank=True, null=True, default=0, help_text="This populates automatically"
    )
    Linked_sold = models.IntegerField(
        blank=True, null=True, default=0, help_text="This populates automatically"
    )
    Quantity_available = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        help_text="This populates automatically (Total - sold - linked_sold)",
    )

    def __str__(self):
        return self.ticket_label


class Ticket(models.Model):
    name = models.CharField(max_length=60, help_text="Customer's Name", default="")
    email = models.CharField(max_length=100, help_text="Customer's Email", default="")
    transaction_ID = models.CharField(
        max_length=100, help_text="Autogenerated transaction ID from STRIPE", default=""
    )
    for_concert = models.ForeignKey(
        Concert, on_delete=models.CASCADE, null=True, default=None
    )
    ticket_type = models.ForeignKey(
        TicketType, on_delete=models.CASCADE, null=True, default=None
    )
    validity = models.BooleanField(
        help_text="If ticked, this ticket is valid.", default=True
    )
    change_log = models.TextField(
        help_text="Will log any changes by automatic systems. I recommend adding any changes here if editing manually.",
        blank=True,
        default="",
    )

    def __str__(self):
        return self.name
