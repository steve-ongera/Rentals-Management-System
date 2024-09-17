
from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('register/', views.custom_register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment_records/', views.tenant_payment_status, name='payment_status'),
    path('add-payment/', views.add_payment, name='add_payment'),
    path('edit-payment/<int:payment_id>/', views.edit_payment, name='edit_payment'),
    path('delete-payment/<int:payment_id>/', views.delete_payment, name='delete_payment'),
    path('my-payment-history/', views.tenant_payment_history, name='tenant_payment_history'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('tenants/', views.tenant_list, name='tenant_list'),
     path('tenant/<int:tenant_id>/', views.tenant_detail, name='tenant_detail'),
    path('tenant/<int:tenant_id>/update/', views.tenant_update, name='tenant_update'),
    path('tenant/<int:tenant_id>/delete/', views.tenant_delete, name='tenant_delete'),
    path('tenant/<int:tenant_id>/maintenance/request/', views.maintenance_request_create, name='maintenance_request_create'),
    path('maintenance/requests/', views.maintenance_request_list, name='maintenance_request_list'),
    path('maintenance/request/<int:request_id>/respond/', views.respond_to_request, name='respond_to_request'),
    path('add_tenant', views.add_tenant , name='add_tenant'),
    path('add_tenant_databse', views.add_tenant_databse , name='add_tenant_databse'),
    path('user_list', views.user_list , name='user_list'),
    path('add_house', views.add_house , name='add_house'),
    path('house_list', views.house_list , name='house_list'),
    path('search-tenant/', views.search_tenant, name='search_tenant'),
    path('search_payment/', views.search_payment, name='search_payment'),
    #######3
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('homepage', views.homepage, name='homepage'),
    path('process/', views.process_query, name='process_query'),

    path('download_receipt/<int:payment_id>/', views.download_receipt, name='download_receipt'),
    #path('payment_generate_pdf/', views.payment_generate_pdf, name='payment_generate_pdf'),
    path('workers/', views.worker_list, name='worker_list'),
    path('workers/<int:id>/', views.worker_detail, name='worker_detail'),
    path('worker/update/<int:worker_id>/', views.update_worker, name='update_worker'),
    path('worker/delete/<int:pk>/', views.delete_worker, name='delete_worker'),
    path('add-worker/', views.add_worker, name='add_worker'),

    path('non-staff/', views.non_staff_list, name='non_staff_list'),
    path('non-staff/add/', views.add_non_staff, name='add_non_staff'),
    path('non-staff/<int:pk>/', views.non_staff_detail, name='non_staff_detail'),

    path('make_payment/', views.tenant_payment, name='tenant_payment'),
    path('payment/confirmation/<int:payment_id>/', views.payment_confirmation, name='payment_confirmation'),

    #path('dashboard/', views.tenant_dashboard, name='tenant_dashboard'),
    path('relocation-request/', views.relocation_request, name='relocation_request'),
    path('apply-leave/', views.apply_leave_notice, name='apply_leave_notice'),
    path('leave-notices/', views.list_leave_notices, name='list_leave_notices'),
    path('respond-leave-notice/<int:notice_id>/', views.respond_leave_notice, name='respond_leave_notice'),
    path('my-leave-notices/', views.tenant_leave_notices, name='tenant_leave_notices'),
    path('leave_notice/delete/<int:notice_id>/', views.delete_leave_notice, name='delete_leave_notice'),
    path('houses/', views.list_houses, name='list_houses'),
    path('houses/<int:house_id>/', views.house_detail, name='house_detail'),
    path('book_house/<int:house_id>/', views.book_house, name='book_house'),
    path('booking_success/', views.booking_success, name='booking_success'),
    path('booked_houses/', views.booked_houses_list, name='booked_houses_list'),
    

    
]

