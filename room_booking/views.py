from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils.text import slugify
from datetime import datetime
from .models import Booking, AvailableTime, Room
from accounts.models import Account
from .forms import RoomForm, AvailableTimeForm
from .utility import booking_time_am_pm_converter
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
                form.save()
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
def add_available_time(request):
    if request.user.is_booking_superadmin:
        if request.method == 'POST':
            form = AvailableTimeForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You have successfully added an available time!')
                return redirect('add_available_time')
            else:
                messages.error(request, 'This time is already filled!')
        context = {
            'current_year': current_year
        }
        return render(request, 'bookings/add_available_time.html', context)
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
def view_available_times(request):
    if request.user.is_booking_superadmin:
        available_times = AvailableTime.objects.all()
        available_times_count = available_times.count()
        context = {
            'available_times': available_times,
            'available_times_count': available_times_count,
            'current_year': current_year
        }
        return render(request, 'bookings/view_available_times.html', context)
    else:
        return redirect('bookings')

@login_required(login_url='login')
def delete_time(request, time_id):
    if request.user.is_booking_superadmin:
        try:
            available_time = AvailableTime.objects.get(id=time_id)
            available_time.delete()
            return redirect('view_available_times')
        except(TypeError, ValueError, OverflowError, Booking.DoesNotExist):
            messages.error(request, 'There is an error! Try again!')
            return redirect('view_available_times')
    else:
        return redirect('bookings')

def create_booking(request):

    room=""
    email=""
    name = ""
    booking_date_val_from = ""
    booking_date_val_to = ""
    description = ""
    booking_time_am_pm_from = None
    booking_time_am_pm_to = None
    available_time_list_from = []
    available_time_list_to = []
    rooms = Room.objects.all()

    if 'book' in request.POST:
        try:
            name = request.POST['name'] 
            room = request.POST['room']
            booking_date_from = request.POST['from_date']
            booking_date_to = request.POST['to_date']
            booking_time_from = request.POST['from_time']
            booking_time_to = request.POST['to_time']
            description = request.POST['description']
            email = request.POST['email']

            if booking_time_from == 'midnight':
                booking_time_from = '12:00 a.m'
            if booking_time_from == 'noon':
                booking_time_from = '12:00 p.m'

            if booking_time_to == 'midnight':
                booking_time_to = '12:00 a.m'
            if booking_time_to == 'noon':
                booking_time_to = '12:00 p.m'

            booking_time_am_pm_from = booking_time_am_pm_converter(booking_time_from)
            booking_time_am_pm_to = booking_time_am_pm_converter(booking_time_to)

            parsed_date_from = datetime.strptime(booking_date_from, "%Y-%d-%m").date()
            parsed_date_to = datetime.strptime(booking_date_to, "%Y-%d-%m").date()
            parsed_time_from = datetime.strptime(booking_time_am_pm_from,"%I:%M %p").time()
            parsed_time_to = datetime.strptime(booking_time_am_pm_to,"%I:%M %p").time()
            booking_time_instance_from = AvailableTime.objects.get(available_time__exact = parsed_time_from)
            booking_time_instance_to = AvailableTime.objects.get(available_time__exact = parsed_time_to)
            room_instance = Room.objects.get(name__exact = room)
            
            try:
                if Account.objects.filter(email=email).exists():
                    if not Booking.objects.filter(booking_time_from=booking_time_instance_from, booking_time_to=booking_time_instance_to, booking_date_from=parsed_date_from, booking_date_to=parsed_date_to, room=room_instance):
                        user = Account.objects.get(email__exact=email)
                        if not name:
                            messages.error(request, 'Please fill all the necessary fields!')
                            return redirect('create_booking')
                        booking = Booking.objects.create(
                            name = name,
                            booking_date_from = parsed_date_from,
                            booking_date_to = parsed_date_to,
                            booking_time_from = booking_time_instance_from,
                            booking_time_to = booking_time_instance_to,
                            room = room_instance,
                            description = description,
                            booking_person = user
                        )
                        # Sending Message when booking
                        current_site = get_current_site(request)
                        mail_subject = 'You have Booked a Meeting Room'
                        message = render_to_string('bookings/booking_email.html',{
                            'user': user,
                            'domain': current_site,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': default_token_generator.make_token(user),
                            'booking_time_from': booking_time_from,
                            'booking_time_to': booking_time_to,
                            'booking_date_from': booking_date_from,
                            'booking_date_to': booking_date_to,
                            'name': name,
                            'description': description,
                            'booking_id': urlsafe_base64_encode(force_bytes(booking.id)),
                        })
                        to_email = email
                        send_email = EmailMessage(mail_subject, message, to=[to_email])
                        if send_email.send():
                            booking.save()
                        messages.success(request, 'Your have successfully booked a meeting room')
                    else:
                        messages.error(request, 'Select other room or change your reservation time and date!')
                        return redirect('create_booking')
                else:
                    messages.error(request, 'Please fill all the necessary fields!')
            except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
                messages.error(request, 'Something went wrong! please try again!')
                return redirect('register')
        except:
                pass
        
    if 'check_time' in request.POST:
        try:
            name = request.POST['name']
            room = request.POST['room']
            email = request.POST['email']
            booking_date_from = request.POST['from_date']
            booking_date_to = request.POST['to_date']
            description = request.POST['description']
            available_times = AvailableTime.objects.all()
            room_instance = Room.objects.get(name__exact = room)
            parsed_date_from = datetime.strptime(booking_date_from, "%Y-%d-%m").date()
            parsed_date_to = datetime.strptime(booking_date_to, "%Y-%d-%m").date()
            booking_date_val_from = booking_date_from
            booking_date_val_to = booking_date_to
            for available_time in available_times:
                if not Booking.objects.filter(booking_time_from=available_time, booking_date_from=parsed_date_from,booking_date_to=parsed_date_to, room=room_instance):
                    available_time_list_from.append(available_time)
            for available_time in available_times:
                if not Booking.objects.filter(booking_time_to=available_time, booking_date_from=parsed_date_from,booking_date_to=parsed_date_to, room=room_instance):
                    available_time_list_to.append(available_time)
        except:
            messages.error(request, 'Something went wrong!')
    context = {
        'rooms': rooms,
        'available_time_list_from': available_time_list_from,
        'available_time_list_to': available_time_list_to,
        'booking_date_val_from': booking_date_val_from,
        'booking_date_val_to': booking_date_val_to,
        'current_year': current_year,
        'name': name,
        'room_val': room,
        'email_val': email,
        'description_val': description,
    }
    return render(request, 'bookings/create_booking.html', context)

@login_required(login_url='login')
def create_booking_from_room(request, room_id):

    name = ""
    booking_date_val_from = ""
    booking_date_val_to = ""
    description = ""
    booking_time_am_pm_from = None
    booking_time_am_pm_to = None
    available_time_list_from = []
    available_time_list_to = []
    room = Room.objects.get(id=room_id)
    if 'book' in request.POST:
        try:
            name = request.POST['name']
            booking_date_from = request.POST['from_date']
            booking_date_to = request.POST['to_date']
            booking_time_from = request.POST['from_time']
            booking_time_to = request.POST['to_time']
            description = request.POST['description']

            if booking_time_from == 'midnight':
                booking_time_from = '12:00 a.m'
            if booking_time_from == 'noon':
                booking_time_from = '12:00 p.m'

            if booking_time_to == 'midnight':
                booking_time_to = '12:00 a.m'
            if booking_time_to == 'noon':
                booking_time_to = '12:00 p.m'
            
            booking_time_am_pm_from = booking_time_am_pm_converter(booking_time_from)
            booking_time_am_pm_to = booking_time_am_pm_converter(booking_time_to)
            
            parsed_date_from = datetime.strptime(booking_date_from, "%Y-%d-%m").date()
            parsed_date_to = datetime.strptime(booking_date_to, "%Y-%d-%m").date()
            parsed_time_from = datetime.strptime(booking_time_am_pm_from,"%I:%M %p").time()
            parsed_time_to = datetime.strptime(booking_time_am_pm_to,"%I:%M %p").time()
            booking_time_instance_from = AvailableTime.objects.get(available_time__exact = parsed_time_from)
            booking_time_instance_to = AvailableTime.objects.get(available_time__exact = parsed_time_to)

            try:
                if not Booking.objects.filter(booking_time_from=booking_time_instance_from, booking_time_to=booking_time_instance_to, booking_date_from=parsed_date_from, booking_date_to=parsed_date_to, room=room):
                    user = request.user
                    if not name:
                        messages.error(request, 'Please fill all the necessary fields!')
                        return HttpResponseRedirect('/bookings/create_booking_from_room/' + room_id)
                    booking = Booking.objects.create(
                        name = name,
                        booking_date_from = parsed_date_from,
                        booking_date_to = parsed_date_to,
                        booking_time_from = booking_time_instance_from,
                        booking_time_to = booking_time_instance_to,
                        room = room,
                        description = description,
                        booking_person = user
                    )
                    current_site = get_current_site(request)
                    mail_subject = 'You have Booked a Meeting Room'
                    message = render_to_string('bookings/booking_email.html',{
                        'user': user,
                        'domain': current_site,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'booking_time_from': booking_time_from,
                        'booking_time_to': booking_time_to,
                        'booking_date_from': booking_date_from,
                        'booking_date_to': booking_date_to,
                        'name': name,
                        'description': description,
                        'booking_id': urlsafe_base64_encode(force_bytes(booking.id)),
                    })
                    to_email = request.user.email
                    send_email = EmailMessage(mail_subject, message, to=[to_email])
                    if send_email.send():
                        booking.save()
                    messages.success(request, 'You have successfully booked a meeting room')
                    return HttpResponseRedirect('/bookings/view_room_information/' + str(room_id))
                else:
                    messages.error(request, 'Something went wrong! Try Again!')
                    return HttpResponseRedirect('/bookings/create_booking_from_room/' + str(room_id))
            except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
                return HttpResponseRedirect('/bookings/create_booking_from_room/' + str(room_id))
        except:
            pass
    if 'check_time' in request.POST:
        try:
            name = request.POST['name']
            booking_date_from = request.POST['from_date']
            booking_date_to = request.POST['to_date']
            description = request.POST['description']
            available_times = AvailableTime.objects.all()
            parsed_date_from = datetime.strptime(booking_date_from, "%Y-%d-%m").date()
            parsed_date_to = datetime.strptime(booking_date_to, "%Y-%d-%m").date()
            booking_date_val_from = booking_date_from
            booking_date_val_to = booking_date_to
            for available_time in available_times:
                if not Booking.objects.filter(booking_time_from=available_time, booking_date_from=parsed_date_from,booking_date_to=parsed_date_to, room=room):
                    available_time_list_from.append(available_time)
            for available_time in available_times:
                if not Booking.objects.filter(booking_time_to=available_time, booking_date_from=parsed_date_from,booking_date_to=parsed_date_to, room=room):
                    available_time_list_to.append(available_time)
        except BaseException as e:
            messages.error(request, e)
    context = {
        'name': name,
        'room': room,
        'available_time_list_from': available_time_list_from,
        'available_time_list_to': available_time_list_to,
        'booking_date_val_from': booking_date_val_from,
        'booking_date_val_to': booking_date_val_to,
        'current_year': current_year,
    }
    return render(request, 'bookings/create_booking_from_room.html', context)

@login_required(login_url='login')
def my_bookings(request):
    meeting_room_booking_info = Booking.objects.filter(booking_person=request.user)
    context = {
        'current_year': current_year,
        'meeting_room_booking_info': meeting_room_booking_info,
    }
    return render(request, 'bookings/my_bookings.html', context)

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
        'booking_time_from': booking.booking_time_from,
        'booking_time_to': booking.booking_time_to,
        'booking_date_from': booking.booking_date_from,
        'booking_date_to': booking.booking_date_to,
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
            'booking_time_from': booking.booking_time_from,
            'booking_time_to': booking.booking_time_to,
            'booking_date_from': booking.booking_date_from,
            'booking_date_to': booking.booking_date_to,
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
                'booking_date_from': booking_info.booking_date_from,
                'booking_date_to': booking_info.booking_date_to,
                'booking_time_from': booking_info.booking_time_from,
                'booking_time_to': booking_info.booking_time_to,
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
