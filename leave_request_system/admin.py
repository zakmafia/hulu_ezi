from django.contrib import admin
from .models import LeaveType, LeaveRequest
# Register your models here.

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ('leave_type',)
    search_fields = ('leave_type',)

@admin.register(LeaveRequest)
class LeaveRequestAdmini(admin.ModelAdmin):
    list_display = ('requester_name','title', 'from_date', 'to_date', 'leave_type', 'created_time')
    search_fields = ('requester_name', 'leave_type',)