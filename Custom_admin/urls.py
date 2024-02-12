from django.contrib import admin
from django.urls import path, include
from Custom_admin.views import *

urlpatterns = [
    path('', admindashboard, name='admindashboard'),
    path('logout/', Logout , name='adminlogout'),
    # path('stocks/', stocks, name='stocks'),
    # path('commodities/', commodities, name='commodities'),
    path('users_data/', users_data, name='users_data'),
    path('Approve/<str:username>/',Approve,name='approve'),
    path('Decline/<str:username>/',Decline,name='decline'),
    path('active_user/', active_user, name='active_user'),
    path('faq/', faq, name='faq'),
    path('error_404/', error_404, name='error_404'),
    path('contact/', contact, name='contact'),
    path('blank/', blank, name='blank'),
    path('admin_profile/', admin_profile, name='admin_profile'),
    path('commodities/silverbeesns/', silverbeesns,name="silverbeesns"),
    path('stocks/itbeesns/', itbeesns,name="itbeesns"),
    path('stocks/sbietfitns/', sbietfitns,name="sbietfitns"),
    path('stocks/niftybeesns/', niftybeesns,name="niftybeesns"),
    path('commodities/goldbeesns/', goldbeesns,name="goldbeesns"),
    path('adminstocksdd/',adminstocksdd, name="adminstocksdropdown"),
    path('admincommoditiesdd/',admincommoditiesdd, name="admincommoditiesdropdown"),
    
]