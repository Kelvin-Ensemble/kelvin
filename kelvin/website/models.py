from django.db import models
from datetime import datetime

# Create your models here.
class Concert(models.Model):
    status_choices = (
        ('OV', 'Over'),
        ('FS','For Sale'),
        ('UC', 'Upcoming'),
        ('SO','Sold Out'),
        ('NY','Not Yet'),
    )
    Concert_Status = models.CharField(max_length=2, choices=status_choices)
    Concert_Date = models.DateTimeField(default=datetime.now, blank=True)


class Ticket_Type(models.Model):
    ticket_label = models.CharField(max_length=40)
    Ticket_ID = models.CharField(max_length=40)
    Linked_Tickets = models.ForeignKey("Ticket_Type", blank=True, null=True)
    def __str__(self):
        return self.ticket_label

class Ticket(models.Model):
    name = models.CharField(max_length=60)
