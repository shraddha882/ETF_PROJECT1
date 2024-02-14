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
     path('stocksindex/tech/', gviews.tech,name="tech"),
      path('stocksindex/psubnk/', gviews.psubnk,name="psubnk"),
       path('stocksindex/nifit/', gviews.nifitetf,name="nifit"),
        path('stocksindex/movalue/', gviews.movalue,name="movalue"),
         path('stocksindex/mafang/', gviews.mafang,name="mafang"),
          path('stocksindex/kotak/', gviews.kotak,name="kotak"),
           path('stocksindex/iti/', gviews.iti,name="iti"),
            path('stocksindex/infrabees/', gviews.infrabees,name="infrabees"),
             path('stocksindex/icicib22/', gviews.icicib22,name="icicib22"),
              path('stocksindex/egold/', gviews.egold,name="egold"),
               path('stocksindex/dspq50/', gviews.dspq50etf,name="dspq50"),
                path('stocksindex/dspit/', gviews.dspitetf,name="dspit"),
                 path('stocksindex/cpse/', gviews.cpseetf,name="cpse"),
                  path('stocksindex/commoi/', gviews.commoietf,name="commoi"),
                   path('stocksindex/axistec/', gviews.axistec,name="axistec"),
                    path('stocksindex/abslnn/', gviews.abslnn50et,name="abslnn"),
    path('stocksdd/',gviews.stocksdd, name="stocksdropdown"),
    path('commoditiesdd/',gviews.commoditiesdd, name="commoditiesdropdown"),
    

]
