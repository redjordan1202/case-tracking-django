import datetime
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator
import datetime

# Create your models here.

class Case(models.Model):
    case_number = models.CharField(max_length=6,primary_key = True, validators=[MinLengthValidator(6)])
    date = models.DateField('date_created')
    order_number = models.CharField(max_length=100)
    rma_type_choices = [
        ('Repair','Repair'), 
        ('Part','Part'),
        ('Replace','Replace')
    ]
    rma_type = models.CharField(max_length = 10, choices=rma_type_choices, default='part')
    part = models.CharField(max_length=256)
    return_label = models.BooleanField()
    tracking_number = models.CharField(max_length=256)
    carrier = models.CharField(max_length=36)
    status_choices = [
        ('TS', 'Tracking Sent'),
        ('CA','Contact Agent'),
        ('CT', 'Check Tracking')
    ]
    status = models.CharField(max_length=2, choices=status_choices)
    case_creator = models.CharField(max_length=256, default='None')
    case_origin = models.CharField(max_length=265, default='None')
    repair_notes = models.TextField(default='None')
    message = models.TextField(default='None')
    case_processed = models.BooleanField()

    def get_age(self):
        now = datetime.date.today()
        date_created = self.date
        age = now - date_created
        return age.days

    age = property(get_age)

    def __str__(self):
        return self.case_number


class Messages(models.Model):
    part_msg = models.TextField()
    repair_msg = models.TextField()
    re_msg = models.TextField()
    part_msg = models.TextField()

