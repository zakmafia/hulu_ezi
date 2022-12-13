from django.db import models

from accounts.models import Account

# Create your models here.
class Room(models.Model):
    name = models.CharField('Room Name',max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    address = models.CharField('Address',max_length=300, blank=True)
    images = models.ImageField('Images',upload_to='photos/rooms')

    def __str__(self):
        return self.name

class AvailableTime(models.Model):
    available_time = models.TimeField('Available Time',unique=True)

    def __str__(self):
        return self.available_time.strftime('%I:%M %p')

class Booking(models.Model):
    name = models.CharField('Booking Name',max_length=120)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date_from = models.DateField('From')
    booking_date_to = models.DateField('To')
    booking_time_from = models.ForeignKey(AvailableTime, on_delete=models.CASCADE, related_name='booking_time_from')
    booking_time_to = models.ForeignKey(AvailableTime, on_delete=models.CASCADE, related_name='booking_time_to')
    description = models.TextField('Description',max_length=255, blank=True)
    booking_person = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.name