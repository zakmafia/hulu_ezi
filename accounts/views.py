from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import RegisterationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from datetime import datetime

# verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
current_year = datetime.now().year

def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegisterationForm()
    context = {
        'form': form,
        'current_year': current_year
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid Login Credentials')
            return redirect('login')
    context = {
        'current_year': current_year
    }
    return render(request, 'accounts/login.html', context)

@login_required(login_url='login')
def logout(request):
    auth.logout(request) 
    messages.success(request, 'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            # Reset Password using email
            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:    
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def manage_user(request):
    users_info = Account.objects.all().order_by('-id')
    context = {
        'users_info': users_info,
        'current_year': current_year
    }
    return render(request, 'accounts/manage_user.html', context)

@login_required(login_url='login')
def edit_user(request, info_id):
    user = Account.objects.get(id=info_id)
    user_manager = user.manager if user.manager else ''
    user_hr = user.hr if user.hr else ''
    all_users = Account.objects.all()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        manager = request.POST['manager']
        hr = request.POST['hr']
        user.first_name = first_name
        user.last_name = last_name
        user.manager = manager
        user.hr = hr
        user.save()
        messages.success(request, 'You have successfully edited the user!')
        return redirect('manage_user')
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'all_users': all_users,
        'user_manager': user_manager,
        'user_hr': user_hr,
        'current_year': current_year
    }
    return render(request, 'accounts/edit_user.html', context)

@login_required(login_url='login')
def search_user(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            users_info = Account.objects.filter(first_name__contains=keyword).order_by('-id')
        context = {
            'users_info': users_info,
            'current_year': current_year,
        }
    return render(request, 'accounts/manage_user.html', context)