from django.contrib import admin
from .models import Room, Booking
# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'address')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    search_fields = ('name', 'address')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_date','to_date', 'room', 'booking_person')
    list_filter = ('room', 'from_date', 'to_date')
    ordering = ('from_date','to_date')
    search_fields = ('name', 'room')


    
