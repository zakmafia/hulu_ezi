from django.urls import path
from . import views

urlpatterns = [
    path('leave_request_page/', views.leave_request_page, name='leave_request_page'),
    path('add_leave_type/', views.add_leave_type, name='add_leave_type'),
    path('view_leave_type/', views.view_leave_type, name='view_leave_type'),
    path('delete_leave_type/<str:leave_type_id>/', views.delete_leave_type, name='delete_leave_type'),
    path('create_leave_request/', views.create_leave_request, name='create_leave_request'),
    path('view_your_leave_request/', views.view_your_leave_request, name='view_your_leave_request'),
    path('users_leave_request/', views.users_leave_request, name='users_leave_request'),
    path('approval_screen/<str:leave_request_id>/', views.approval_screen, name='approval_screen'),
    path('hr_users_leave_request/', views.hr_users_leave_request, name='hr_users_leave_request'),
    path('hr_approval_screen/<str:leave_request_id>/', views.hr_approval_screen, name="hr_approval_screen"),
    path('all_users_request/', views.all_users_request, name='all_users_request'),
    path('detail_approved_user/<str:requester_name_id>/', views.detail_approved_user, name='detail_approved_user'),
    path('search/', views.search, name='search'),

    path('export_report/', views.export_report, name='export_report'),
    path('export_report_user/<str:user_id>/', views.export_report_user, name='export_report_user'),
]