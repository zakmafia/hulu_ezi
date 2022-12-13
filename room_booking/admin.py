from django.contrib import admin
from .models import Room, Booking, AvailableTime
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'address')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'booking_date_from','booking_date_to', 'room', 'booking_person')
    list_filter = ('room', 'booking_date_from', 'booking_date_to')
    ordering = ('booking_date_from','booking_date_to')
    search_fields = ('name', 'room')

@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('available_time',)

    
