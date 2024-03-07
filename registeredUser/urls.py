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

    # path('account-verify/<token>',views.accout_verify, name='account-verify'),
    # path('userstocksdd/',views.userstocksdd, name="userstocksdropdown"),
    path('usercommoditiesdd/',views.usercommoditiesdd, name="usercommoditiesdropdown"),
    path('usertransactions/',views.Usertrans, name="usertrans"),
    path('userbuyhistory/', views.user_buy_trans, name='user_buy_history'),
    path('userallhistory/', views.useralltrans, name='user_all_history'),
    path('usersellhistory/', views.user_sell_trans, name='user_sell_history'),
    path('selletf/', views.usersell, name = 'sell_etf'),
    # path('buy_sell/', views.buy_sell, name = 'buy_sell'),
    
]
