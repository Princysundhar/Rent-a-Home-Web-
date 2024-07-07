"""Rent_A_Home URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',views.log),
    path('log_post',views.log_post),
    path('logout',views.logout),
    path('admin_home',views.admin_home),
    path('user_home',views.user_home),
    path('forgot_password',views.forgot_password),
    path('forgot_password_post',views.forgot_password_post),
    path('change_password',views.change_password),
    path('change_password_post',views.change_password_post),
    path('view_user',views.view_user),
    path('block_user/<id>',views.block_user),
    path('unblock_user/<id>',views.unblock_user),
    path('view_complaint',views.view_complaint),
    path('send_reply/<id>',views.send_reply),
    path('send_reply_post/<id>',views.send_reply_post),
    path('view_home_and_verify',views.view_home_and_verify),
    path('accept_home/<id>',views.accept_home),
    path('reject_home/<id>',views.reject_home),
    
#========================================================================== USER
    path('user_register',views.user_register),
    path('user_register_post',views.user_register_post),
    path('user_change_password',views.user_change_password),
    path('user_change_password_post',views.user_change_password_post),
    path('add_home',views.add_home),
    path('add_home_post',views.add_home_post),
    path('view_home',views.view_home),
    path('edit_home/<id>',views.edit_home),
    path('edit_home_post/<id>',views.edit_home_post),
    path('delete_home/<id>',views.delete_home),
    path('view_home_and_send_request',views.view_home_and_send_request),
    path('send_request/<id>',views.send_request),
    path('view_request_and_verify',views.view_request_and_verify),
    path('accept_request/<id>',views.accept_request),
    path('reject_request/<id>',views.reject_request),
    path('view_approved_request_owner',views.view_approved_request_owner),
    path('upload_document/<id>',views.upload_document),
    path('upload_document_post/<id>',views.upload_document_post),
    path('view_approved_request_user',views.view_approved_request_user),
    path('view_document/<id>',views.view_document),
    path('make_payment/<id>/<amount>',views.make_payment),
    path('view_payment',views.view_payment),
    path('view_payment_post',views.view_payment_post),
    path('send_complaint',views.send_complaint),
    path('send_complaint_post',views.send_complaint_post),
    path('user_view_reply',views.user_view_reply),
    path('on_payment_success/<id>',views.on_payment_success),

]
