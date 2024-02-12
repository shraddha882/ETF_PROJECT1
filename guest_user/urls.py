from django.contrib import admin
from django.urls import path
from guest_user import views as gviews
from registeredUser import views as rviews
import guest_user
urlpatterns = [
    path('',gviews.home,name = 'index'),
    path('login/',rviews.user_login, name='login'),
    path('account-verify/<token>',rviews.accout_verify, name='account-verify'),
    path('stocksindex/',gviews.stocksIndex,name='stocksindex'),
    path('commoditiesindex/',gviews.commoditiesIndex,name='commoditiesindex'),
    path('stocksindex/niftybees/', gviews.niftybees,name="niftybees"),
    path('stocksindex/goldbees/', gviews.goldbees,name="goldbees"),
    path('stocksindex/silverbees/', gviews.silverbees,name="silverbees"),
    path('stocksindex/itbees/', gviews.itbees,name="itbees"),
    path('stocksindex/sbietfit/', gviews.sbietfit,name="sbietfit"),
    path('stocksdd/',gviews.stocksdd, name="stocksdropdown"),
    path('commoditiesdd/',gviews.commoditiesdd, name="commoditiesdropdown"),
    

]
