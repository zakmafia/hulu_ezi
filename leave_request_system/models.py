from django.db import models
from accounts.models import Account
import uuid

# Create your models here.
class LeaveType(models.Model):
    leave_type = models.CharField('Leave Type',max_length=120, unique=True)
    detail = models.TextField('Detail', max_length=255, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.leave_type

class LeaveRequest(models.Model):
    title = models.CharField('Title',max_length=150)
    detail = models.TextField('Detail',max_length=255, blank=True)
    from_date = models.DateField('From')
    to_date = models.DateField('To')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    requester_name = models.ForeignKey(Account, on_delete=models.CASCADE)
    pending_manager_approval = models.BooleanField('Pending Manager Approval', default=True)
    pending_hr_approval = models.BooleanField('Pending HR Approval', default=True)
    manager_approved = models.BooleanField('Manager Approved', default=False)
    hr_approved = models.BooleanField('HR Approved', default=False)
    manager_comment = models.TextField('Manager Comment', max_length=255, blank=True)
    hr_comment = models.TextField('HR Comment', max_length=255, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return self.title

