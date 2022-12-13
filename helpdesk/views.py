from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Staff, Role, Priority, UserRequest, Issue, KnowledgeBase, KnowledgeCategory, Ticket
from accounts.models import Account
from .forms import StaffForm, RoleForm, PriorityForm, UserRequestForm, IssueForm, KnowledgeBaseForm, TicketForm
# For Sending Email message
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
# Create your views here.
current_year = datetime.now().year

def helpdesk_home(request):
    context = {
        'current_year': current_year,
    }
    return render(request, 'helpdesk/helpdesk_home.html', context)

# Priority
@login_required(login_url='login')
def create_priority(request):
    if request.method == 'POST':
        form = PriorityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have sucessfully created a status')
            return redirect('create_priority')
        else:
            messages.error(request, 'This priority already exists')
    else:
        form = PriorityForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_priority.html', context)

@login_required(login_url='login')
def view_priority(request):
    priorities = Priority.objects.all()
    context = {
        'current_year': current_year,
        'priorities': priorities
    }
    return render(request, 'helpdesk/view_priority.html', context)

@login_required(login_url='login')
def delete_priority(request, priority_id):
    if request.user.is_superadmin:
        priority = Priority.objects.get(id=priority_id)
        priority.delete()
        messages.success(request, 'You have successfully deleted the priority!')
        return redirect('view_priority')
    else:
        return redirect('helpdesk_home')

# Role
@login_required(login_url='login')
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have sucessfully created a role')
            return redirect('create_role')
        else:
            messages.error(request, 'This role already exists')
    else:
        form = RoleForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_role.html', context)

@login_required(login_url='login')
def view_role(request):
    roles = Role.objects.all()
    context = {
        'current_year': current_year,
        'roles': roles
    }
    return render(request, 'helpdesk/view_role.html', context)

@login_required(login_url='login')
def delete_role(request, role_id):
    if request.user.is_superadmin:
        role = Role.objects.get(id=role_id)
        role.delete()
        messages.success(request, 'You have successfully deleted the role!')
        return redirect('view_role')
    else:
        return redirect('helpdesk_home')

# Staff
@login_required(login_url='login')
def create_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have sucessfully created a staff')
            return redirect('create_staff')
        else:
            messages.error(request, 'This staff already exists')
    else:
        form = StaffForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_staff.html', context)

@login_required(login_url='login')
def view_staff(request):
    staff_list = Staff.objects.all()
    context = {
        'current_year': current_year,
        'staff_list': staff_list,
    }
    return render(request, 'helpdesk/view_staff.html', context)

@login_required(login_url='login')
def delete_staff(request, staff_id):
    if request.user.is_superadmin:
        staff_member = Staff.objects.get(id=staff_id)
        staff_member.delete()
        messages.success(request, 'You have successfully deleted the staff member!')
        return redirect('view_staff')
    else:
        return redirect('helpdesk_home')

# Issue
@login_required(login_url='login')
def create_issue(request):
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have sucessfully created an issue')
            return redirect('create_issue')
        else:
            messages.error(request, 'This issue already exists')
    else:
        form = IssueForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_issue.html', context)

@login_required(login_url='login')
def view_issue(request):
    issues = Issue.objects.all()
    context = {
        'current_year': current_year,
        'issues': issues
    }
    return render(request, 'helpdesk/view_issue.html', context)

@login_required(login_url='login')
def delete_issue(request, issue_id):
    if request.user.is_superadmin:
        issue = Issue.objects.get(id=issue_id)
        issue.delete()
        messages.success(request, 'You have successfully deleted the issue!')
        return redirect('view_issue')
    else:
        return redirect('helpdesk_home')
    

# UserRequest
@login_required(login_url='login')
def create_user_request(request):
    if request.method == 'POST':
        form = UserRequestForm(request.POST, request.FILES)
        if form.is_valid():
            user_request = form.save(commit=False)
            user_request.requester = request.user
            user_request.save()
            messages.success(request, 'You have successfully created a request. You will hear from us shortly')
            return redirect('create_user_request')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        form = UserRequestForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_user_request.html', context)

@login_required(login_url='login')
def my_request(request):
    my_requests = UserRequest.objects.filter(requester=request.user).order_by('-id')  
    context = {
        'current_year': current_year,
        'my_requests': my_requests
    }
    return render(request, 'helpdesk/my_request.html', context)

@login_required(login_url='login')
def view_user_request(request):
    all_requests = UserRequest.objects.all().order_by('-id')
    context = {
        'current_year': current_year,
        'all_requests': all_requests,
    }
    return render(request, 'helpdesk/view_user_request.html', context)

# Tickets
@login_required(login_url='login')
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data['task']
            assigned_person = form.cleaned_data['assigned_person']
            priority = form.cleaned_data['priority']
            allocated_date = form.cleaned_data['allocated_date']
            deadline = form.cleaned_data['deadline']
            name = Account.objects.get(email=assigned_person).first_name
            mail_subject = 'You have a new ticket assigned'
            message = render_to_string('helpdesk/ticket_email.html', {
                'task': task,
                'priority': priority,
                'allocated_date': allocated_date,
                'deadline': deadline,
                'name': name
            })
            to_email = assigned_person
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            form.save()
            messages.success(request, 'You have successfully created a ticket.')
            return redirect('create_ticket')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        form = TicketForm

    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_ticket.html', context)

@login_required(login_url='login')
def view_ticket(request):
    tickets = Ticket.objects.all().order_by('-id')
    priorities = Priority.objects.all()
    context = {
        'current_year': current_year,
        'tickets': tickets,
        'priorities': priorities
    }
    return render(request, 'helpdesk/view_ticket.html', context)

@login_required(login_url='login')
def edit_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully edited the ticket')
            return redirect('view_ticket')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        form = TicketForm(instance=ticket)
    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/edit_ticket.html', context)

@login_required(login_url='login')
def delete_ticket(request, ticket_id):
    if request.user.is_superadmin:
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.delete()
        messages.success(request, 'You have successfully deleted the ticket')
        return redirect('view_ticket')
    else:
        return redirect('helpdesk_home')

# Manage
@login_required(login_url='login')
def manage_helpdesk(request):
    context = {
        'current_year': current_year,
    }
    return render(request, 'helpdesk/manage_helpdesk.html', context)

# FAQ
@login_required(login_url='login')
def view_faq(request):
    context = {
        'current_year': current_year
    }
    return render(request, 'helpdesk/view_faq.html', context)

# Knowledge Base
@login_required(login_url='login')
def create_kb(request):
    if request.method == 'POST':
        form = KnowledgeBaseForm(request.POST, request.FILES)
        if form.is_valid():
            category = KnowledgeCategory.objects.get(id=request.POST['category'])
            newdoc = form.save(commit=False)
            newdoc.docfile = request.FILES['docfile']
            newdoc.category = category
            newdoc.save()
            messages.success(request, 'You have successfully added a new document.')
        else:
            messages.error(request, 'This file already exists.')
    else:
        form = KnowledgeBaseForm
    context = {
        'current_year': current_year,
        'form': form
    }
    return render(request, 'helpdesk/create_kb.html', context)

@login_required(login_url='login')
def view_kb(request):
    documents = KnowledgeBase.objects.all().order_by('-id')
    knowledge_categories = KnowledgeCategory.objects.all().order_by('-id')
    context = {
        'current_year': current_year,
        'documents': documents,
        'knowledge_categories': knowledge_categories,
    }
    return render(request, 'helpdesk/view_kb.html', context)

@login_required(login_url='login')
def delete_kb(request, doc_docfile_id):
    if request.user.is_superadmin:
        kb = KnowledgeBase.objects.get(id=doc_docfile_id)
        kb.delete()
        messages.success(request, 'You have successfully deleted the document!')
        return redirect('view_kb')
    else:
        return redirect('helpdesk_home')

@login_required(login_url='login')
def search_kb(request):
    knowledge_categories = KnowledgeCategory.objects.all().order_by('-id')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            documents = KnowledgeBase.objects.filter(docfile__contains=keyword).order_by('-id')
        context = {
            'current_year': current_year,
            'documents': documents,
            'knowledge_categories': knowledge_categories,
        }
    return render(request, 'helpdesk/view_kb.html', context)

@login_required(login_url='login')
def search_by_cat(request, cat_name):
    knowledge_categories = KnowledgeCategory.objects.all().order_by('-id')
    documents = KnowledgeBase.objects.filter(category__name=cat_name)
    context = {
        'current_year': current_year,
        'knowledge_categories': knowledge_categories,
        'documents': documents,
    }
    return render(request, 'helpdesk/view_kb.html', context)
    