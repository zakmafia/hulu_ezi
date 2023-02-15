from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking, name='bookings'),
    path('add_rooms/', views.add_rooms, name='add_rooms'),
    path('view_rooms/', views.view_rooms, name='view_rooms'),
    path('edit_room/<str:room_id>/', views.edit_room, name='edit_room'),
    path('delete_room/<str:room_id>/', views.delete_room, name='delete_room'),
    path('view_room_information/<str:room_id>/', views.view_room_information, name='view_room_information'),

    path('my_bookings/', views.my_bookings, name='my_bookings'),
    path('create_booking/<str:room_id>/', views.create_booking, name='create_booking'),
    path('cancel_booking_validate/<uidb64>/<token>/<booking_id>/', views.cancel_booking_validate, name='cancel_booking_validate'),
    path('cancel_booking_view/', views.cancel_booking_view, name='cancel_booking_view'),
    path('cancel_booking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('cancel_booking_user/<str:info_id>/', views.cancel_booking_user, name='cancel_booking_user'),
    path('cancel_booking_admin/<str:info_id>/<str:room_id>/', views.cancel_booking_admin, name='cancel_booking_admin'),
]
