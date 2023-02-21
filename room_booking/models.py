from django.db import models
import uuid
from accounts.models import Account

# Create your models here.
class Room(models.Model):
    name = models.CharField('Room Name',max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    address = models.CharField('Address',max_length=500, blank=True)
    images = models.ImageField('Images',upload_to='photos/rooms')
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField('Booking Name',max_length=120)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    from_date = models.DateField('From Date')
    to_date = models.DateField('To Date')
    from_time = models.TimeField('From Time')
    to_time = models.TimeField('To Time')
    description = models.TextField('Description',max_length=255, blank=True, null=True)
    booking_person = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    active_booking = models.BooleanField('Active', default=True)

    def __str__(self):
        return self.name