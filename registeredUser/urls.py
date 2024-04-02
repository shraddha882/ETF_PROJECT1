from django.contrib import admin
from django.urls import path
from registeredUser import views

urlpatterns = [
    # path('',views.home,name = 'index'),
    path('login/', views.user_login,name="Userlogin"),
    path('logout/', views.Logout,name="Userlogout"),
    path('register/', views.register,name="register"),
    path('UserDashboard/', views.Userdashboard,name="UserDashboard"),
    path('UserBlank/', views.Userbuy,name="UserBuy"),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('stocks/', views.userstocks, name='userstocks'),
    # path('commodities/', views.usercommodities, name='usercommodities'),
    path('etftables/<str:table>/', views.etftables,name="etftables"),
    path('usercommoditiesdd/',views.usercommoditiesdd, name="usercommoditiesdropdown"),
    path('usertransactions/',views.Usertrans, name="usertrans"),
    path('usertransdetails/', views.userbuydetails, name='userbuydetails'),
    path('userallhistory/', views.useralldetails, name='useralldetails'),
    path('usersellhistory/', views.userselldetails, name='userselldetails'),
    path('selletf/', views.usersell, name = 'sell_etf'),
    path('subs/', views.subs, name = 'subs'),
    # path('buy_sell/', views.buy_sell, name = 'buy_sell'),
    
]
