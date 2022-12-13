from django.contrib import admin
from .models import Priority, Issue, Role, Staff, UserRequest, KnowledgeBase, Weight, Status, Ticket, KnowledgeCategory

# Register your models here.
@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    search_fields = ('name', 'priority')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('member', 'role')
    search_fields = ('member', 'role')

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'issue', 'other_issue', 'created_on')
    search_fields = ('requester', 'issue', 'other_issue', 'created_on')

@admin.register(KnowledgeCategory)
class KnowledgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_diplay = ('docfile', 'category')
    search_fields = ('docfile', 'category')

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('task', 'priority', 'assigned_person', 'allocated_date', 'status')
    search_fields = ('task', 'priority', 'assigned_person', 'allocated_date', 'status')