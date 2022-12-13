import email
import io
import xlsxwriter 
from datetime import datetime
from django.http import FileResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import LeaveTypeForm
from .models import LeaveType, LeaveRequest
from accounts.models import Account
# For leave request message
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
# Create your views here.
current_year = datetime.now().year


@login_required(login_url='login')
def leave_request_page(request):
    return render(request, 'leave_request_system/leave_request_page.html')

@login_required(login_url='login')
def add_leave_type(request):
    if request.method == 'POST':
        form = LeaveTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'You have successfully create a leave type')
            return redirect('add_leave_type')
        else:
            messages.error(request, 'Leave with this name already exists!')
    else:
        form = LeaveTypeForm
    context = {
        'form': form,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/add_leave_type.html', context)

@login_required(login_url='login')
def view_leave_type(request):
    leave_types = LeaveType.objects.all()
    leave_types_count = leave_types.count()
    context = {
        'leave_types': leave_types,
        'leave_types_count':leave_types_count,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/view_leave_type.html', context)

@login_required(login_url='login')
def delete_leave_type(request, leave_type_id):
    try:
        leave_type = LeaveType.objects.get(id=leave_type_id)
        leave_type.delete()
        return redirect('view_leave_type')
    except(TypeError, ValueError, OverflowError, LeaveType.DoesNotExist):
        messages.error(request, 'There is an error! Try again!')
        return redirect('view_leave_type')


@login_required(login_url='login')
def create_leave_request(request):
    user = request.user
    leave_types = LeaveType.objects.all()
    if request.method == 'POST':
        try:
            title = request.POST['title']
            detail = request.POST['detail']
            from_date = request.POST['from_date']
            to_date = request.POST['to_date']
            leave_type = request.POST['leave_type']
            requester_name = request.user

            parsed_from_date = datetime.strptime(from_date, "%Y-%d-%m").date()
            parsed_to_date = datetime.strptime(to_date, "%Y-%d-%m").date()
            leave_type_instance = LeaveType.objects.get(leave_type=leave_type)
            leave_request = LeaveRequest.objects.create(
                title=title,
                detail=detail,
                from_date=parsed_from_date,
                to_date=parsed_to_date,
                leave_type=leave_type_instance,
                requester_name=requester_name
            )
            user_hr_email = user.hr
            hr_mail_subject = 'A new leave request'
            message_to_hr = render_to_string('leave_request_system/message_to_hr.html', {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'title': title,
                'from_date': from_date,
                'to_date': to_date,
                'leave_type': leave_type
            })
            hr_to_email = user_hr_email
            send_email_to_hr = EmailMessage(hr_mail_subject, message_to_hr, to=[hr_to_email])
            leave_request.save()
            send_email_to_hr.send()  
            messages.success(
                    request, 'You have successfully created a leave request!')
        except(TypeError, ValueError, OverflowError) as e:
            messages.error(request, e)
    context = {
        'leave_types': leave_types,
    }
    return render(request, 'leave_request_system/create_leave_request.html', context)


@login_required(login_url='login')
def view_your_leave_request(request):
    user = request.user
    leave_requests = LeaveRequest.objects.filter(requester_name=user).order_by('-id')

    context = {
        'leave_requests': leave_requests,
        'current_year': current_year
    }

    return render(request, 'leave_request_system/view_your_leave_request.html', context)


@login_required(login_url='login')
def users_leave_request(request):
    leave_request_list = []
    leave_requests = LeaveRequest.objects.filter(pending_manager_approval=True, hr_approved=True).order_by('-id')
    for leave_request in leave_requests:
        if leave_request.requester_name.manager == request.user.email:
            leave_request_list.append(leave_request)

    context = {
        'leave_request_list': leave_request_list,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/users_leave_request.html', context)


@login_required(login_url='login')
def all_users_request(request):
    leave_requests = LeaveRequest.objects.filter(manager_approved=True, hr_approved=True).order_by('-id')
    context = {
        'leave_requests': leave_requests,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/all_users_request.html', context)


@login_required(login_url='login')
def approval_screen(request, leave_request_id):
    leave_request = LeaveRequest.objects.get(id=leave_request_id)
    if 'approve' in request.POST:
        comment = request.POST['comment']
        leave_request.manager_comment = comment
        leave_request.pending_manager_approval = False
        leave_request.manager_approved = True
        mail_subject = 'Manager Approval(Approved)'
        message = render_to_string('leave_request_system/manager_approval_email.html',{
            'first_name': leave_request.requester_name.first_name,
            'last_name': leave_request.requester_name.last_name,
            'title': leave_request.title,
            'from_date': leave_request.from_date,
            'to_date': leave_request.to_date,
            'leave_type': leave_request.leave_type,
            'manager_comment': leave_request.manager_comment,
        })
        to_email = leave_request.requester_name.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        leave_request.save()
        return redirect('users_leave_request')
    if 'reject' in request.POST:
        comment = request.POST['comment']
        leave_request.manager_comment = comment
        leave_request.pending_manager_approval = False
        leave_request.pending_hr_approval = False
        leave_request.manager_approved = False
        mail_subject = 'Manager Approval(Rejected)'
        message = render_to_string('leave_request_system/manager_rejected_email.html',{
            'first_name': leave_request.requester_name.first_name,
            'last_name': leave_request.requester_name.last_name,
            'title': leave_request.title,
            'from_date': leave_request.from_date,
            'to_date': leave_request.to_date,
            'leave_type': leave_request.leave_type,
            'manager_comment': leave_request.manager_comment,
        })
        to_email = leave_request.requester_name.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        leave_request.save()
        return redirect('users_leave_request')
    context = {
        'leave_request': leave_request,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/approval_screen.html', context)


@login_required(login_url='login')
def hr_users_leave_request(request):
    leave_request_list = []
    leave_requests = LeaveRequest.objects.filter(pending_hr_approval=True).order_by('-id')
    for leave_request in leave_requests:
        if leave_request.requester_name.hr == request.user.email:
            leave_request_list.append(leave_request)
    context = {
        'leave_request_list': leave_request_list,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/hr_users_leave_request.html', context)


@login_required(login_url='login')
def hr_approval_screen(request, leave_request_id):
    leave_request = LeaveRequest.objects.get(id=leave_request_id)
    if 'approve' in request.POST:
        comment = request.POST['comment']
        leave_request.hr_comment = comment
        leave_request.pending_hr_approval = False
        leave_request.hr_approved = True
        mail_subject = 'HR Approval(Approved)'
        manager_mail_subject = 'A new leave request (HR Approved)'
        message = render_to_string('leave_request_system/hr_approval_email.html',{
            'first_name': leave_request.requester_name.first_name,
            'last_name': leave_request.requester_name.last_name,
            'title': leave_request.title,
            'from_date': leave_request.from_date,
            'to_date': leave_request.to_date,
            'leave_type': leave_request.leave_type,
            'hr_comment': leave_request.hr_comment,
        })
        message_to_manager = render_to_string('leave_request_system/message_to_manager.html', {
                'first_name': leave_request.requester_name.first_name,
                'last_name': leave_request.requester_name.last_name,
                'title': leave_request.title,
                'from_date': leave_request.from_date,
                'to_date': leave_request.to_date,
                'leave_type': leave_request.leave_type,
        })
        manager_to_email = leave_request.requester_name.manager
        to_email = leave_request.requester_name.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email_to_manager = EmailMessage(manager_mail_subject, message_to_manager, to=[manager_to_email])
        send_email.send()
        send_email_to_manager.send()  
        leave_request.save()
        return redirect('hr_users_leave_request')
    if 'reject' in request.POST:
        comment = request.POST['comment']
        leave_request.hr_comment = comment
        leave_request.pending_hr_approval = False
        leave_request.pending_manager_approval = False
        leave_request.hr_approved = False
        mail_subject = 'HR Approval(Rejected)'
        message = render_to_string('leave_request_system/hr_rejected_email.html',{
            'first_name': leave_request.requester_name.first_name,
            'last_name': leave_request.requester_name.last_name,
            'title': leave_request.title,
            'from_date': leave_request.from_date,
            'to_date': leave_request.to_date,
            'leave_type': leave_request.leave_type,
            'hr_comment': leave_request.hr_comment,
        })
        to_email = leave_request.requester_name.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()
        leave_request.save()
        return redirect('hr_users_leave_request')
    context = {
        'leave_request': leave_request,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/hr_approval_screen.html', context)

@login_required(login_url='login')
def export_report(request):
    leave_requests = LeaveRequest.objects.filter(manager_approved=True, hr_approved=True).order_by('-id')
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    cell_format = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0,5,30)
    worksheet.write('A1', 'Name', cell_format)
    worksheet.write('B1', 'Email', cell_format)
    worksheet.write('C1', 'Title', cell_format)
    worksheet.write('D1', 'From date', cell_format)
    worksheet.write('E1', 'To date', cell_format)
    worksheet.write('F1', 'Leave Type', cell_format)
    n = 2
    for i in leave_requests:
        worksheet.write(f'A{n}', f'{ i.requester_name.first_name } { i.requester_name.last_name }')
        worksheet.write(f'B{n}', f'{ i.requester_name.email }')
        worksheet.write(f'C{n}', f'{ i.title }')
        worksheet.write(f'D{n}', f'{ i.from_date }')
        worksheet.write(f'E{n}', f'{ i.to_date }')
        worksheet.write(f'F{n}', f'{ i.leave_type }')
        n += 1
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report.xlsx')

@login_required(login_url='login')
def detail_approved_user(request, requester_name_id):
    user = Account.objects.get(id=requester_name_id)
    leave_requests = LeaveRequest.objects.filter(requester_name=user,manager_approved=True, hr_approved=True).order_by('-id')
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'leave_requests': leave_requests,
        'current_year': current_year,
        'user_id': user.id, 
    }
    
    return render(request, 'leave_request_system/detail_approved_user.html', context)

@login_required(login_url='login')
def export_report_user(request, user_id):
    user = Account.objects.get(id=user_id)
    leave_requests = LeaveRequest.objects.filter(manager_approved=True, hr_approved=True, requester_name=user).order_by('-id')
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    cell_format = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet()
    worksheet.set_column(0,5,30)
    worksheet.write('A1', 'Name', cell_format)
    worksheet.write('B1', 'Email', cell_format)
    worksheet.write('C1', 'Title', cell_format)
    worksheet.write('D1', 'From date', cell_format)
    worksheet.write('E1', 'To date', cell_format)
    worksheet.write('F1', 'Leave Type', cell_format)
    n = 2
    for i in leave_requests:
        worksheet.write(f'A{n}', f'{ i.requester_name.first_name } { i.requester_name.last_name }')
        worksheet.write(f'B{n}', f'{ i.requester_name.email }')
        worksheet.write(f'C{n}', f'{ i.title }')
        worksheet.write(f'D{n}', f'{ i.from_date }')
        worksheet.write(f'E{n}', f'{ i.to_date }')
        worksheet.write(f'F{n}', f'{ i.leave_type }')
        n += 1
    workbook.close()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='report_single_user.xlsx')

@login_required(login_url='login')
def search(request):
    leave_requests = LeaveRequest.objects.filter(manager_approved=True, hr_approved=True).order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            leave_requests = LeaveRequest.objects.filter(manager_approved=True, hr_approved=True, requester_name__first_name__contains=keyword).order_by('-id')
    context = {
        'leave_requests': leave_requests,
        'current_year': current_year,
    }
    return render(request, 'leave_request_system/all_users_request.html', context)