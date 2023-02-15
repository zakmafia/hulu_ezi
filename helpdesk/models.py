import os
import uuid
from django.db import models
from django.conf import settings
from accounts.models import Account
# Create your models here.

class Priority(models.Model):
    name = models.CharField('Priority', max_length=50, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = 'priority'
        verbose_name_plural = 'priorities'

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField('Role', max_length=50, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Staff(models.Model):
    member = models.OneToOneField(Account, on_delete=models.CASCADE)
    role = models.OneToOneField(Role, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'

    def __str__(self):
        return self.member.email

class Issue(models.Model):
    name = models.CharField('Issue', max_length=50, unique=True)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class UserRequest(models.Model):
    requester = models.ForeignKey(Account, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, blank=True, null=True)
    is_other_issue = models.BooleanField('Is Other Issue', default=False)
    other_issue = models.CharField('Other Issue', max_length=50, blank=True)
    issue_description = models.TextField('Issue Description', max_length=255, blank=True)
    image = models.ImageField('Image', upload_to='photos/user_requests', blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.requester.email

class Weight(models.Model):
    name = models.CharField('Weight Name', max_length=255, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField('Status Name', max_length=255, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statuses'

    def __str__(self):
        return self.name

class Ticket(models.Model):
    task = models.CharField('Task', max_length=255)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    assigned_person = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    allocated_date = models.DateField('Allocated Date')
    deadline = models.DateField('Deadline Date')
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    completion_date = models.DateField('Completion Date', blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.task

class KnowledgeCategory(models.Model):
    name = models.CharField('Category', max_length=255, unique=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        verbose_name = 'knowledge category'
        verbose_name_plural = 'knowledge categories'

    def __str__(self):
        return self.name

class KnowledgeBase(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    category = models.ForeignKey(KnowledgeCategory, on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    def __str__(self):
        return self.docfile.name
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.docfile.name))
        super(KnowledgeBase, self).delete(*args, **kwargs)
