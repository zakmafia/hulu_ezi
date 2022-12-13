from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='bookings'),
    path('add_rooms/', views.add_rooms, name='add_rooms'),
    path('add_available_time/', views.add_available_time, name='add_available_time'),
    path('view_rooms/', views.view_rooms, name='view_rooms'),
    path('view_available_times/', views.view_available_times, name='view_available_times'),
    path('delete_room/<room_id>/', views.delete_room, name='delete_room'),
    path('delete_time/<time_id>/', views.delete_time, name='delete_time'),
    path('view_room_information/<room_id>/', views.view_room_information, name='view_room_information'),

    path('create_booking/', views.create_booking, name='create_booking'),
    path('create_booking_from_room/<room_id>/', views.create_booking_from_room, name='create_booking_from_room'),
    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('cancel_booking_validate/<uidb64>/<token>/<booking_id>/', views.cancel_booking_validate, name='cancel_booking_validate'),
    path('cancel_booking_view/', views.cancel_booking_view, name='cancel_booking_view'),
    path('cancel_booking/<booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel_booking_user/<info_id>/', views.cancel_booking_user, name='cancel_booking_user'),
    path('cancel_booking_admin/<info_id>/<room_id>/', views.cancel_booking_admin, name='cancel_booking_admin'),
]
