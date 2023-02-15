from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.text import slugify
from django.db.models import Q
from datetime import datetime
from .models import Booking, Room
from accounts.models import Account
from .forms import RoomForm, BookingForm
# For booking message
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
current_year = datetime.now().year

def booking(request):
    rooms = Room.objects.all()
    rooms_count = rooms.count()
    context = {
        'current_year': current_year,
        'rooms': rooms,
        'rooms_count': rooms_count,
    }
    return render(request, 'bookings/bookings.html', context)

@login_required(login_url='login')
def add_rooms(request):
    if request.user.is_booking_superadmin:
        if request.method == 'POST':
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                room = form.save(commit=False)
                room.slug = slugify(room.name)
                room.save()
                messages.success(request, 'You have successfully added a room!')
                return redirect('add_rooms')
            else:
                messages.error(request, 'Room with this name already exists!')
        else:
            form = RoomForm
        context = {
            'form': form,
            'current_year': current_year,
        }
        return render(request, 'bookings/add_rooms.html', context)
    else:
        return redirect('bookings')

@login_required(login_url='login')
def view_rooms(request):
    if request.user.is_booking_superadmin:
        rooms = Room.objects.all()
        rooms_count = rooms.count()
        context = {
            'rooms': rooms,
            'current_year': current_year,  
            'rooms_count': rooms_count,  
        }
        return render(request, 'bookings/view_rooms.html', context)
    else:
        return redirect('bookings')

@login_required(login_url='login')
def edit_room(request, room_id):
    if request.user.is_booking_superadmin:
        room = Room.objects.get(id=room_id)
        form = RoomForm(instance=room)
        if request.method == 'POST':
            form = RoomForm(request.POST, request.FILES, instance=room)
            if form.is_valid():
                room = form.save(commit=False)
                room.slug = slugify(room.name)
                room.save()
                messages.success(request, 'You have successfully edited the room!')
                return HttpResponseRedirect('/bookings/edit_room/' + str(room_id))
            else:
                messages.error(request, 'Something went wrong!')
        context = {
            'form': form,
            'current_year': current_year
        }
        return render(request, 'bookings/edit_room.html', context)
    else:
        return redirect('bookings')

@login_required(login_url='login')
def delete_room(request, room_id):
    if request.user.is_booking_superadmin:
        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return redirect('view_rooms')
        except(TypeError, ValueError, OverflowError, Room.DoesNotExist):
            messages.error(request, 'There is an error! Try again!')
            return redirect('view_rooms')
    else:
        return redirect('bookings')

def view_room_information(request, room_id):
    room = Room.objects.get(id=room_id)
    meeting_room_booking_info = Booking.objects.filter(room=room).order_by('-id')
    context = {
        'room': room,
        'meeting_room_booking_info': meeting_room_booking_info,
        'current_year': current_year,
    }
    return render(request, 'bookings/view_room_info.html', context)

@login_required(login_url='login')
def my_bookings(request):
    meeting_room_booking_info = Booking.objects.filter(booking_person=request.user)
    context = {
        'current_year': current_year,
        'meeting_room_booking_info': meeting_room_booking_info,
    }
    return render(request, 'bookings/my_bookings.html', context)

@login_required(login_url='login')
def create_booking(request, room_id):
    form = BookingForm()
    booking_person = request.user
    room = Room.objects.get(id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if not Booking.objects.filter(
                Q(room=room),

                Q(from_date=booking.from_date, to_date=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) | 
                Q(from_date=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) | 

                Q(from_date=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) |
                Q(from_date=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |

                Q(to_date=booking.from_date ,from_time=booking.from_time, to_time=booking.to_time) |
                Q(to_date=booking.from_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(to_date=booking.from_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |
                
                Q(from_date=booking.from_date, to_date__lte=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date=booking.from_date, to_date__lte=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) | 
                Q(from_date=booking.from_date, to_date__lte=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) | 
                
                Q(from_date=booking.from_date, to_date__gte=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date=booking.from_date, to_date__gte=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |
                Q(from_date=booking.from_date, to_date__gte=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) |

                Q(from_date__lte=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date__lte=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |
                Q(from_date__lte=booking.from_date, to_date=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) |

                Q(from_date__gte=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date__gte=booking.from_date, to_date=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |
                Q(from_date__gte=booking.from_date, to_date=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) |

                Q(from_date__lte=booking.from_date, to_date__gte=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date__lte=booking.from_date, to_date__gte=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) | 
                Q(from_date__lte=booking.from_date, to_date__gte=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time) | 

                Q(from_date__gte=booking.from_date, to_date__lte=booking.to_date ,from_time__lte=booking.from_time, to_time__gte=booking.from_time) |
                Q(from_date__gte=booking.from_date, to_date__lte=booking.to_date ,from_time__lte=booking.to_time, to_time__gte=booking.to_time) |
                Q(from_date__gte=booking.from_date, to_date__lte=booking.to_date ,from_time=booking.from_time, to_time=booking.to_time)
                ):
                if booking.from_date > booking.to_date:
                    messages.error(request, 'From date cannot be greater than To date')
                    return HttpResponseRedirect('/bookings/create_booking/' + str(room_id))

                if booking.from_time > booking.to_time:
                    messages.error(request, 'From time cannot be greater than To time')
                    return HttpResponseRedirect('/bookings/create_booking/' + str(room_id))
                booking.booking_person = booking_person
                booking.room = room
                current_site = get_current_site(request)
                mail_subject = 'You have Booked a Meeting Room'
                message = render_to_string('bookings/booking_email.html',{
                        'user': request.user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
                        'token': default_token_generator.make_token(request.user),
                        'booking_time_from': booking.from_time,
                        'booking_time_to': booking.to_time,
                        'booking_date_from': booking.from_date,
                        'booking_date_to': booking.to_date,
                        'name': booking.name,
                        'description': booking.description,
                        'booking_id': urlsafe_base64_encode(force_bytes(booking.id)),
                    })
                to_email = request.user.email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                if send_email.send():
                    booking.save()
                messages.success(request, 'You have booked a Meeting Room')
                return HttpResponseRedirect('/bookings/view_room_information/' + str(room_id))
            else:
                messages.error(request, 'Booking made with the same time and date')
                return HttpResponseRedirect('/bookings/create_booking/' + str(room_id))
           

    context = {'form': form, 'room': room, 'current_year': current_year}
    return render(request, 'bookings/create_booking.html', context)


def cancel_booking_validate(request, uidb64, token, booking_id):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
        booking_id_code = urlsafe_base64_decode(booking_id).decode()
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        request.session['booking_id'] = booking_id_code
        messages.success(request, 'You have cancelled your booking!')
        return redirect('cancel_booking_view')
    else:
        return redirect('create_booking_view')

def cancel_booking_view(request):
    try:
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        booking_id = request.session.get('booking_id')
        user_booking = Booking.objects.filter(booking_person=user, id=booking_id)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    context = {
        'user_booking': user_booking,
    }
    return render(request, 'bookings/cancel_booking_view.html', context) 

def cancel_booking_user(request, info_id):
    booking = Booking.objects.get(id=info_id)
    mail_subject = 'You have successfully cancelled your meeting room booking!'
    message = render_to_string('bookings/cancelled_booking_email.html', {
        'user': request.user,
        'name': booking.name,
        'room': booking.room,
        'booking_time_from': booking.from_time,
        'booking_time_to': booking.to_time,
        'booking_date_from': booking.from_date,
        'booking_date_to': booking.to_date,
        })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    booking.delete()
    send_email.send()
    return redirect('my_bookings')

def cancel_booking(request, booking_id):
    try:
        uid = request.session.get('uid')
        user = Account.objects.get(pk=uid)
        booking = Booking.objects.get(id=booking_id)
        current_site = get_current_site(request)
        mail_subject = 'You have successfully cancelled your meeting room booking!'
        message = render_to_string('bookings/cancelled_booking_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'name': booking.name,
            'room': booking.room,
            'booking_time_from': booking.from_time,
            'booking_time_to': booking.to_time,
            'booking_date_from': booking.from_date,
            'booking_date_to': booking.to_date,
            'booking_id': urlsafe_base64_encode(force_bytes(booking.id)),
        })
        to_email = booking.booking_person.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        if send_email.send():
            booking.delete()
            return redirect('cancel_booking_view')
    except(TypeError, ValueError, OverflowError, Booking.DoesNotExist):
        return redirect('create_booking')

@login_required(login_url='login')
def cancel_booking_admin(request, info_id, room_id):
    if request.user.is_booking_admin:
        booking_info = Booking.objects.get(id=info_id, room=room_id)
        if request.method == 'POST':
            reason = request.POST['reason']
            mail_subject = 'Meeting Room Booking Cancellation'
            message = render_to_string('bookings/admin_cancellation_booking.html',{
                'booking_person_name': booking_info.booking_person.first_name,
                'name': booking_info.name,
                'booking_date_from': booking_info.from_date,
                'booking_date_to': booking_info.to_date,
                'booking_time_from': booking_info.from_time,
                'booking_time_to': booking_info.to_time,
                'admin_name': request.user.first_name,
                'reason': reason
            })
            to_email = booking_info.booking_person.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            if send_email.send():
                booking_info.delete()
                return HttpResponseRedirect('/bookings/view_room_information/' + str(room_id))
        context = {
            'booking_info': booking_info,
        }
        return render(request, 'bookings/cancel_booking_admin_view.html', context)
    else:
        return redirect('bookings')
