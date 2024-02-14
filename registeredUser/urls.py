from django.contrib import admin
from django.urls import path
from registeredUser import views

urlpatterns = [
    # path('',views.home,name = 'index'),
    path('login/', views.user_login,name="Userlogin"),
    path('logout/', views.Logout,name="Userlogout"),
    path('register/', views.register,name="register"),
    path('UserDashboard/', views.Userdashboard,name="UserDashboard"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('stocks/', views.userstocks, name='userstocks'),
    # path('commodities/', views.usercommodities, name='usercommodities'),
    path('niftybees/', views.NIFTYbees,name="NIFTYbees"),
    path('goldbees/', views.GOLDbees,name="GOLDbees"),
    path('silverbees/', views.SILVERbees,name="SILVERbees"),
    path('itbees/', views.ITbees,name="ITbees"),
    path('sbietfit/', views.SBIetfit,name="SBIetfit"),
    # path('account-verify/<token>',views.accout_verify, name='account-verify'),
    # path('userstocksdd/',views.userstocksdd, name="userstocksdropdown"),
    path('usercommoditiesdd/',views.usercommoditiesdd, name="usercommoditiesdropdown"),
    
    
]
