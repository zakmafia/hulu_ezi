from django.urls import path
from . import views

urlpatterns = [
    path('', views.helpdesk_home, name='helpdesk_home'),

    path('create_staff/', views.create_staff, name='create_staff'),
    path('view_staff/', views.view_staff, name='view_staff'),
    path('delete_staff/<str:staff_id>/', views.delete_staff, name='delete_staff'),

    path('create_priority/', views.create_priority, name='create_priority'),
    path('view_priority/', views.view_priority, name='view_priority'),
    path('delete_priority/<str:priority_id>/', views.delete_priority, name='delete_priority'),

    path('create_role/', views.create_role, name='create_role'),
    path('view_role/', views.view_role, name='view_role'),
    path('delete_role/<str:role_id>/', views.delete_role, name='delete_role'),

    path('create_issue/', views.create_issue, name='create_issue'),
    path('view_issue/', views.view_issue, name='view_issue'),
    path('edit_issue/<str:issue_id>/', views.edit_issue, name='edit_issue'),
    path('delete_issue/<str:issue_id>/', views.delete_issue, name='delete_issue'),

    path('create_user_request/', views.create_user_request, name='create_user_request'),
    path('my_request/', views.my_request, name='my_request'),
    path('view_user_request/', views.view_user_request, name='view_user_request'),
    path('detail_my_request/<str:my_request_id>/', views.detail_my_request, name='detail_my_request'),
    path('detail_user_request/<str:user_request_id>/', views.detail_user_request, name='detail_user_request'),

    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('view_ticket/', views.view_ticket, name='view_ticket'),
    path('edit_ticket/<str:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('delete_ticket/<str:ticket_id>/', views.delete_ticket, name='delete_ticket'),
    
    path('manage_helpdesk/', views.manage_helpdesk, name='manage_helpdesk'),

    path('view_faq/', views.view_faq, name='view_faq'),
    path('create_kb/', views.create_kb, name='create_kb'),
    path('view_kb/', views.view_kb, name='view_kb'),
    path('delete_kb/<str:doc_docfile_id>/', views.delete_kb, name='delete_kb'),
    path('search_kb/', views.search_kb, name='search_kb'),
    path('search_kb_by_cat/<str:cat_name>/', views.search_kb_by_cat, name='search_kb_by_cat'),
    path('search_role/', views.search_role, name='search_role'),
    path('search_priority/', views.search_priority, name='search_priority'),
    path('search_staff/', views.search_staff, name='search_staff'),
    path('search_issue/', views.search_issue, name='search_issue'),

    
]