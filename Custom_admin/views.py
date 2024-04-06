from django.shortcuts import render
from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as loginuser, authenticate, logout ,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from registeredUser.models import RegisteredUser, Wallet
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
from Custom_admin.models import *
from datetime import datetime,date
from django.db.models import Q
from django.db.models import Avg
from datetime import timedelta, date
from django.db.models import Sum, Avg, Max
from datetime import timedelta, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import json, datetime
from django.db.models import Sum, Avg, Max, Case, When, F,FloatField, Value
from django.db.models.functions import Coalesce, Cast
from django.http import HttpResponseRedirect
import datetime


def admindashboard(request):
        return render(request, 'admindashboard.html')
        

def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('Userlogin')


def admin_profile(request):
    admin_details = {
        'full_name': 'Yashika Thakur',
        'job': 'Web Developer',
        'phone': '123-456-7890',
        'email': 'yashiksthriya31@gmail.com',
    }
    context = {'admin_details': admin_details}
    return render(request, 'admin_profile.html', context)


def delete_profile(request, profile_id):
    # profile_instance = get_object_or_404(profile_model, id=profile_id)

    # if request.method == 'POST':
    #     profile_instance.delete()
    #     return redirect('admin_profile')

    return HttpResponse("Invalid request method for delete")


def update(request, id):
    return render(request, 'admin_profile.html')


# @login_required
def users_data(request):
        users = RegisteredUser.objects.all()
        wallet = Wallet.objects.all()
        return render(request, 'users_data.html', {'users': users,'wallet':wallet})
    
from django.db import transaction
# @login_required
# def Approve(request,username):
#     update=RegisteredUser.objects.get(username=username)
#     user=User.objects.get(username=username)
#     if user is not None:
#         update.login_status=True
#         update.save()
#         messages.success(request, f'{username} is now allowed to Login')  
#     else:
#         update.delete()
#     return redirect('users_data')

# # @login_required
# def Decline(request,username):
#     update=RegisteredUser.objects.get(username=username)
#     user=User.objects.get(username=username)
#     if user is not None:    
#         update.login_status=False
#         update.save()
#         messages.error(request, f'{username} is not allowed to Login')
#     else:
#         update.delete()
#     return redirect('users_data')

def Approve(request, username):
    update = get_object_or_404(RegisteredUser, username=username)
    update.login_status = True
    update.save()
    messages.success(request, f'{username} is now allowed to login')
    return redirect('users_data')
  

def Decline(request, username):
    update = get_object_or_404(RegisteredUser, username=username)
    update.login_status = False
    update.save()
    messages.error(request, f'{username} is not allowed to login')
    return redirect('users_data')

def delete_selected_users(request):
    if request.method == 'GET' and 'usernames' in request.GET:
        usernames = request.GET.get('usernames').split(',')
        # Delete selected users
        deleted_users = RegisteredUser.objects.filter(username__in=usernames)
        deleted_users_count = deleted_users.count()
        deleted_usernames = ", ".join([user.username for user in deleted_users])
        deleted_users.delete()
        # Add a success message
        messages.success(request, f"{deleted_users_count} user(s) ({deleted_usernames}) deleted successfully.")
        # Redirect back to the user details page
        return redirect('users_data')
    else:
        # Handle other cases, like POST requests
        pass



 


def active_user(request):
    active_registered_users = RegisteredUser.objects.filter(login_status=True, is_verified=True)
    wallet = Wallet.objects.all()

    if request.method == 'POST':
        # Load the request body as JSON
        data = json.loads(request.body)
        subscription_type = data.get('subscriptionType')
        time_period = data.get('timePeriod')
        selected_usernames = data.get('selectedUsernames', [])  # Get selected usernames
        
        # Loop through selected usernames
        for username in selected_usernames:
            reg = RegisteredUser.objects.get(username=username)
            wallet_instance, created = Wallet.objects.get_or_create(user=reg)
            
            # Check if subscriptionType or timePeriod is provided
            if subscription_type is not None or subscription_type != 'Select Subscriptions':
                wallet_instance.sub_status = subscription_type
                
            if time_period is not None or time_period != 'Select Months':
                # Use the start_date to calculate the end_date
                start_date = timezone.now()
                wallet_instance.start_date = start_date
                end_date = None
                
                if time_period == '1 month':
                    end_date = start_date + timezone.timedelta(days=30)
                elif time_period == '3 months':
                    end_date = start_date + timezone.timedelta(days=90)
                elif time_period == '6 months':
                    end_date = start_date + timezone.timedelta(days=180)
                elif time_period == '1 year':
                    end_date = start_date + timezone.timedelta(days=365)
                
                # Calculate remaining days if end_date is defined
                remaining_days = None
                if end_date:
                    remaining_days = (end_date - timezone.now()).days
                    if remaining_days < 0:
                        remaining_days = 0
                
                # Update period and end_date
                wallet_instance.period = time_period
                wallet_instance.end_date = end_date
                wallet_instance.remaining_days = remaining_days
                
            # Save the changes to the wallet
            wallet_instance.save()
            
            # Check if current date is equal to end date
            if wallet_instance.end_date and timezone.now().date() == wallet_instance.end_date.date():
                # Revert subscription status and period to default values
                wallet_instance.sub_status = 'Unsubscribed'
                wallet_instance.period = '1 month'
                wallet_instance.end_date = None
                wallet_instance.remaining_days = None
                # Other fields can be set to None or default values as needed
                
                # Save the changes to the wallet
                wallet_instance.save()
                
        return redirect('active_user')  # Redirect back to the same view after saving changes
    
    context = {
        'data': active_registered_users,
        'wallet': wallet,
    }
 
    return render(request, 'active_user.html', context)

def aggregate_buy_transactions(user_instance):
    return (
        UserBuyetf.objects.filter(Username=user_instance, trans_type='BUY')
        .values('Etf_purchased__Etfnames')
        .annotate(
            total_quantity=Sum('Quantity'),
            total_cost=Sum('Cost'),
            latest_date=Max('Date_time')  # Annotate latest date
        )
    )

def aggregate_sell_transactions(user_instance):
    return (
        UserBuyetf.objects.filter(Username=user_instance, trans_type='SELL')
        .values('Etf_purchased__Etfnames')
        .annotate(
            total_quantity=Sum('Quantity'),
            total_cost=Sum('Cost'),
            latest_date=Max('Date_time')
        )
    )

def aggregate_all_transactions(user_instance):
    return (
        UserBuyetf.objects.filter(Username=user_instance)
        .values('Etf_purchased__Etfnames')
        .annotate(
            total_quantity=Sum(
                Case(
                    When(trans_type='BUY', then=F('Quantity')),
                    When(trans_type='SELL', then=-F('Quantity')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            total_cost=Sum(
                Case(
                    When(trans_type='BUY', then=F('Cost')),
                    When(trans_type='SELL', then=-F('Cost')),
                    default=0,
                    output_field=FloatField()
                )
            ),
            latest_date=Max('Date_time')
        )
    )

def calculate_percent_diff(current_price, mod_avg):
    if mod_avg != 0:
        return (current_price - mod_avg) / mod_avg * 100
    else:
        return 0.0

def admintrans(request):

    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print(data)
            user = data.get('name')
            user_instance = RegisteredUser.objects.get(username=user)
            # print(user_instance)
        except RegisteredUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        aggregated_data_buy = aggregate_buy_transactions(user_instance)
        modified_data_buy = modify_data(aggregated_data_buy)


        aggregated_data_sell = aggregate_sell_transactions(user_instance)
        modified_data_sell = modify_data(aggregated_data_sell)
    
        aggregated_data_all = aggregate_all_transactions(user_instance)
        modified_data_all = modify_data(aggregated_data_all)
        # print(modified_data_all)
        context = {
            'data_all': modified_data_all,
            'data_buy': modified_data_buy,
            'data_sell': modified_data_sell,
            }

        return JsonResponse({'dataall':list(modified_data_all)})

    
def modify_data(aggregated_data):
    # Create a dictionary to hold aggregated data for each ETF
    aggregated_data_dict = {}
    for entry in aggregated_data:
        etfname = entry['Etf_purchased__Etfnames']
        if etfname not in aggregated_data_dict:
            aggregated_data_dict[etfname] = {
                'Etf_purchased__Etfnames': etfname,
                'total_quantity': entry['total_quantity'],
                'total_cost': entry['total_cost'],
                'latest_date': entry['latest_date']
            }
        else:
            # Accumulate total quantity and cost
            aggregated_data_dict[etfname]['total_quantity'] += entry['total_quantity']
            aggregated_data_dict[etfname]['total_cost'] += entry['total_cost']
            
    # Modify aggregated data and create context
    modified_data = []
    for etfname, entry in aggregated_data_dict.items():
        entry['mod_date'] = entry['latest_date'].date()  # Update mod_date
        entry['etf_name'] = entry['Etf_purchased__Etfnames']  # Add ETF name
        # Add other required fields like current price, average cost, percent difference, etc.
        # Fetch current price for each ETF
        try:
            current_price = AllETF.objects.get(Etfnames=etfname).close
        except AllETF.DoesNotExist:
            current_price = 0.0  # Set the price to 0 if ETF not found
        
        entry['current_price'] = current_price  # Add current price
        entry['mod_avg'] = entry['total_cost'] / entry['total_quantity'] if entry['total_quantity'] != 0 else 0.0  # Calculate average cost
        current_price = entry['current_price']
        entry['percent_diff'] = calculate_percent_diff(current_price, entry['mod_avg'])  # Calculate percent difference
        entry['20dma'], entry['etf_close_minus_20dma'], entry['etf_close_div_20dma'] = calculate_20dma([etfname])  # Calculate 20 DMA
        entry['50dma'], entry['etf_close_minus_50dma'], entry['etf_close_div_50dma'] = calculate_50dma([etfname])  # Calculate 50 DMA
        entry['100dma'], entry['etf_close_minus_100dma'], entry['etf_close_div_100dma'] = calculate_100dma([etfname])  # Calculate 100 DMA
        modified_data.append(entry)

    return modified_data


def deactivate_user(request):
    deactivate_registered_users = RegisteredUser.objects.filter(login_status=False)
    context ={
         'data': deactivate_registered_users
    }
    return render(request, 'deactivate_user.html', context)


def adminbuydetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = data.get('username')

            etfname = etf_name.upper()
            try:
                etf_model = globals()[etfname]
            except KeyError:
                return JsonResponse({'error': 'Invalid ETF name'}, status=400)
            
            # Fetch only SELL transactions
            detailed_data = UserBuyetf.objects.filter(Username__username=username,Etf_purchased__Etfnames=etf_name, trans_type='Buy').values('Date_time', 'Quantity', 'Cost', 'Purchase_close_value', 'trans_type')
            
            for entry in detailed_data:
                entry['Date'] = entry['Date_time'].date()
                
                try:
                    # Fetch current price of the ETF
                    curr_price = AllETF.objects.get(Etfnames=etf_name).close
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'ETF data not found'}, status=400)
                
                # Calculate current cost and percentage difference
                curr_cost = curr_price * entry['Quantity']
                entry['CurrPrice'] = curr_price
                entry['CurrCost'] = curr_cost
                entry['PercentDiff'] = ((curr_cost - entry['Cost']) / entry['Cost']) * 100
                
            return JsonResponse({'detailed_data': list(detailed_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def adminselldetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = data.get('username')
            etfname = etf_name.upper()
            try:
                etf_model = globals()[etfname]
            except KeyError:
                return JsonResponse({'error': 'Invalid ETF name'}, status=400)
            
            # Fetch only SELL transactions
            detailed_data = UserBuyetf.objects.filter(Username__username=username,Etf_purchased__Etfnames=etf_name, trans_type='SELL').values('Date_time', 'Quantity', 'Cost', 'Purchase_close_value', 'trans_type')
            
            for entry in detailed_data:
                entry['Date'] = entry['Date_time'].date()
                
                try:
                    # Fetch current price of the ETF
                    curr_price = AllETF.objects.get(Etfnames=etf_name).close
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'ETF data not found'}, status=400)
                
                # Calculate current cost and percentage difference
                curr_cost = curr_price * entry['Quantity']
                entry['CurrPrice'] = curr_price
                entry['CurrCost'] = curr_cost
                entry['PercentDiff'] = ((curr_cost - entry['Cost']) / entry['Cost']) * 100
                
            return JsonResponse({'detailed_data': list(detailed_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def adminalldetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = data.get('username')
            etfname = etf_name.upper()
            print(username)
            try:
                etf_model = globals()[etfname]
            except KeyError:
                return JsonResponse({'error': 'Invalid ETF name'}, status=400)
            
            
            detailed_data = UserBuyetf.objects.filter(Username__username=username,Etf_purchased__Etfnames=etf_name).values('Date_time', 'Quantity', 'Cost', 'Purchase_close_value','trans_type')
            
            for entry in detailed_data:
                entry['Date'] = entry['Date_time'].date()
                
                try:
                    # Fetch current price of the ETF
                    curr_price = AllETF.objects.get(Etfnames=etf_name).close
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'ETF data not found'}, status=400)
                
                # Calculate current cost and percentage difference
                curr_cost = curr_price * entry['Quantity']
                entry['CurrPrice'] = curr_price
                entry['CurrCost'] = curr_cost
                entry['PercentDiff'] = ((curr_cost - entry['Cost']) / entry['Cost']) * 100
                
            return JsonResponse({'detailed_data': list(detailed_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def adminbuyhistory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            etfname = etf_name.upper()
            
            try:
                etf_model = globals()[etfname]
            except KeyError:
                return JsonResponse({'error': 'Invalid ETF name'}, status=400)

            detailed_data = UserBuyetf.objects.filter(Etf_purchased__Etfnames=etf_name).values('Date_time', 'Quantity', 'Cost', 'Purchase_close_value')
            
            for entry in detailed_data:
                entry['Date'] = entry['Date_time'].date()
                
                try:
                    # Fetch current price of the ETF
                    curr_price = AllETF.objects.get(Etfnames=etf_name).close
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'ETF data not found'}, status=400)
                
                # Calculate current cost and percentage difference
                curr_cost = curr_price * entry['Quantity']
                entry['CurrPrice'] = curr_price
                entry['CurrCost'] = curr_cost
                entry['PercentDiff'] = ((curr_cost - entry['Cost']) / entry['Cost']) * 100
                
            return JsonResponse({'detailed_data': list(detailed_data)})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# def commodities(request):
#     return render(request, 'commodities.html')

 


# def active_user(request):
#     return render(request, 'active_user.html')


def faq(request):
    return render(request, 'faq.html')


def blank(request):
    return render(request, 'blank.html')


def error_404(request):
    return render(request, 'error_404.html')


def contact(request):
    return render(request, 'contact.html')

# def niftybeesns(request):
#     table_name = 'NIFTYBEES'
#     category = 'Stocks'
#     alldata = NIFTYBEES_NS.objects.all()
#     data = list(alldata)
#     calculate_percentage_diff(data)

#     if request.method == 'POST':
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')
#         print(start_date_str, end_date_str)

#         if start_date_str and end_date_str:
#             # Convert string dates to datetime objects
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#             queryset = alldata.filter(date__range=[start_date, end_date])
#             data = list(queryset)
#             calculate_percentage_diff(data)
#             print(start_date, end_date)
#             context = {
#                 'data': queryset,
#                   'table_name':table_name,
#                     'category':category
                
#             }
#             return render(request, 'adminNifty.html', context)
#         else:
#             # If start_date or end_date is not provided, show all data
#             context = {
#                 'data': alldata,
#                   'table_name':table_name,
#                     'category':category
#             }
#             return render(request, 'adminNifty.html', context)

#     # Default behavior: show all data
#     context = {
#                 'data': alldata,
#                'table_name':table_name,
#                  'category':category
               
#                }
#     return render(request,'adminNifty.html',context)

def niftybeesns(request):
    table_name = 'NIFTYBEES'
    category = 'Stocks'
    alldata = NIFTYBEES_NS.objects.all()
    data = list(alldata)
    calculate_percentage_diff(data)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str, end_date_str)

        if start_date_str and end_date_str:
            # Convert string dates to datetime objects
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = alldata.filter(date__range=[start_date, end_date])
            data = list(queryset)
            calculate_percentage_diff(data)
            print(start_date, end_date)
            context = {
                'data': queryset,
                'table_name': table_name,
                'category': category
            }
            return render(request, 'adminNifty.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                'table_name': table_name,
                'category': category
            }
            return render(request, 'adminNifty.html', context)

    # Default behavior: show all data
    context = {
        'data': alldata,
        'table_name': table_name,
        'category': category
    }
    return render(request, 'adminNifty.html', context)

def itbeesns(request):
    table_name = 'ITBEES'
    category = 'Stocks'
    alldata = ITBEES_NS.objects.all()
    data = list(alldata)
    calculate_percentage_diff(data)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str, end_date_str)

        if start_date_str and end_date_str:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = alldata.filter(date__range=[start_date, end_date])
            data = list(queryset)
            calculate_percentage_diff(data)
            print(start_date, end_date)
            context = {
                'data': queryset,
                  'table_name':table_name,
                    'category':category
            }
            return render(request, 'adminIt.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                'table_name':table_name,
                  'category':category
            }
            return render(request, 'adminIt.html', context)

    # Default behavior: show all data
    context = {
        'data': alldata,
        'table_name':table_name,
          'category':category
               }
    return render(request,'adminIt.html',context)

def sbietfitns(request):
    table_name = 'SBIETFIT'
    
    alldata = SBIETFIT_NS.objects.all()
    data = list(alldata)
    calculate_percentage_diff(data)
    category = 'Stocks'

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str, end_date_str)

        if start_date_str and end_date_str:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = alldata.filter(date__range=[start_date, end_date])
            calculate_percentage_diff(data)
            print(start_date, end_date)
            print(start_date, end_date)
            context = {
                'data': queryset,
                 'table_name':table_name,
                   'category':category
            }
            return render(request, 'adminSbi.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                 'table_name':table_name,
                   'category':category
            }
            return render(request, 'adminSbi.html', context)

    # Default behavior: show all data
    context = {'data': alldata,
               'table_name':table_name,
                 'category':category
               }
    return render(request,'adminSbi.html',context)






def goldbeesns(request):
    table_name = 'GOLDBEES'
    category= 'Commodities'

    alldata = GOLDBEES_NS.objects.all()
    data = list(alldata)
    calculate_percentage_diff(data)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str, end_date_str)

        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = alldata.filter(date__range=[start_date, end_date])
            data = list(queryset)
            calculate_percentage_diff(data)

            context = {
                'data': data,
                'table_name': table_name,
                'category':category
            }
            return render(request, 'adminGold.html', context)
        else:
            context = {
                'data': data,
                'table_name': table_name,
                  'category':category
            }
            return render(request, 'adminGold.html', context)

    context = {
        'data': data,
        'table_name': table_name,
          'category':category
    }
    return render(request, 'adminGold.html', context)

def silverbeesns(request):
        table_name = 'SILVERBEES'
        category= 'Commodities'
        alldata = SILVERBEES_NS.objects.all()
        data = list(alldata) 
        calculate_percentage_diff(data)

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)

                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminSilver.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminSilver.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                     'category':category
                   }
        return render(request,'adminSilver.html',context)

def egoldns(request):
        table_name = 'EGOLD'
        category= 'Commodities'
        alldata = EGOLD_NS.objects.all()
        data = list(alldata) 
        calculate_percentage_diff(data)


        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminegold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                     'category':category
                }
                return render(request, 'adminegold.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                    'category':category
                   }
        return render(request, 'adminegold.html', context)



def abslnn50etns(request):
        table_name = 'ABSLNN50ET'
        alldata = ABSLNN50ET_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'
        

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category

                }
                return render(request, 'adminabslnn50et.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminabslnn50et.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                    'category':category
                   }
        return render(request, 'adminabslnn50et.html', context)

def commoietfns(request):
        table_name = 'COMMOIETF'
        alldata = COMMOIETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                     'category':category
                }
                return render(request, 'admincommoietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                     'category':category
                }
                return render(request, 'admincommoietf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                    'category':category
                   }
        return render(request, 'admincommoietf.html', context)


def cpseetfns(request):
        table_name = 'CPSEETF'
        alldata = COMMOIETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admincpseetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admincpseetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'admincpseetf.html', context)


def dspitetfns(request):
        table_name = 'DSPITETF'
        alldata = DSPITETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admindspitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admindspitetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'admindspitetf.html', context)



def dspq50etfns(request):
        table_name = 'DSPQ50ETF'
        alldata = DSPQ50ETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admindspq50.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'admindspq50.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'admindspq50.html', context)

def axistecns(request):
        table_name = 'AXISTEC'
        alldata = AXISTECETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminaxistec.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminaxistec.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'adminaxistec.html', context)


def icicib22ns(request):
        table_name = 'ICICIB22'
        alldata = ICICIB22_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminicicib22.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminicicib22.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'adminicicib22.html', context)


def infrabeesns(request):
        table_name = 'INFRABEES'
        alldata = INFRABEES_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'admininfrabees.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'admininfrabees.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'admininfrabees.html', context)


def itins(request):
        table_name = 'ITI'
        alldata = ITIETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminiti.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                    'category':category
                }
                return render(request, 'adminiti.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category
                   }
        return render(request, 'adminiti.html', context)


def kotakns(request):
        table_name = 'KOTAK'
        alldata = KOTAKPSUBK_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'


        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminkotak.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminkotak.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'adminkotak.html', context)

def mafangns(request):
        table_name = 'MAFANG'
        alldata = MAFANG_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminmafang.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminmafang.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'adminmafang.html', context)


def movaluens(request):
        table_name = 'MOVALUE'
        alldata = MOVALUE_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'
        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminmovalue.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminmovalue.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'adminmovalue.html', context)


def nifitetfns(request):
        table_name = 'NIFITETF'
        alldata = NIFITETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminnifitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminnifitetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'adminnifitetf.html', context)

def psubnkns(request):
        table_name = 'PSUBNKIETF'
        alldata = PSUBNKIETF_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'
        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminpsubnkietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'adminpsubnkietf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'adminpsubnkietf.html', context)




def techns(request):
        table_name = 'TECH'
        alldata = TECH_NS.objects.all()
        data = list(alldata)
        calculate_percentage_diff(data)
        category = 'Stocks'

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'admintechetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name,
                   'category':category

                }
                return render(request, 'admintechetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name,
                   'category':category

                   }
        return render(request, 'admintechetf.html', context)


def stocks(request):
    category = 'Stocks'
    stocks1 = 'NIFTYBEES'
    stocks2 = 'ITBEES'
    stocks3 = 'SBIETFIT'
    stocks4 = 'TECH'
   
    stocks5 = 'ABSLNN50ET'
    stocks6 = 'CPSEETF'
    stocks7 = 'MAFANG'
    stocks8 = 'MOVALUE'
    stocks9 = 'NIFITETF'
    stocks10 = 'PSUBNKIETF'
    stocks11 = 'ICICIB22'
    stocks12  = 'DSPITETF'
    stocks13 = 'COMMOIETF'
    stocks14 = 'ITIETF'
    stocks15 = 'AXISTECETF'
    stocks16 = 'KOTAKPSUBK'
    stocks17 = 'DSPQ50ETF'
    stocks18 = 'INFRABEES'
    alldata = AllETF.objects.all()
    # etf_names = AllETF.objects.all().values('Etfnames' ,flat=True)
    # etf_name_list = list(etf_names.values())
    # print(etf_name_list)
    etf_names = AllETF.objects.all().values_list('Etfnames', flat=True)
    etf_name_list = list(etf_names)
    

    etf_data, etf_close_minus_20dma, etf_close_div_20dma = calculate_20dma(etf_name_list)
    etf_data_50dma, etf_close_minus_50dma, etf_close_div_50dma  = calculate_50dma(etf_name_list)
    etf_data_100dma, etf_close_minus_100dma, etf_close_div_100dma = calculate_100dma(etf_name_list)

    
    # print(alldata)
    

    context = {
        'data':alldata,
        'etf_data':etf_data,
        'etf_close_minus_20dma': etf_close_minus_20dma,
        'etf_close_div_20dma': etf_close_div_20dma,
        'etf_data_50dma':etf_data_50dma,
        'etf_close_minus_50dma': etf_close_minus_50dma,
        'etf_close_div_50dma': etf_close_div_50dma,
        'etf_data_100dma': etf_data_100dma,
        'etf_close_minus_100dma': etf_close_minus_100dma,
        'etf_close_div_100dma': etf_close_div_100dma,
        'nifty':stocks1,
        'it':stocks2,
        'sbi':stocks3,
        'tech':stocks4,
        'abslnn':stocks5,
        'cpse':stocks6,
        'mafang':stocks7,
        'movalue':stocks8,
        'nifit':stocks9,
        'psubnk':stocks10,
        'icicib22':stocks11,
        'dspit':stocks12,
        'commoi':stocks13,
        'iti':stocks14,
        'axistec':stocks15,
        'kotakp':stocks16,
        'dspq50':stocks17,
        'infrabees':stocks18,
        'category':category

    }
    return render(request, 'stocks.html',context)



# def adminstocksdd(request):
     
#     category = 'Stocks'
#     stocks1 = 'NIFTYBEES'
#     stocks2 = 'ITBEES'
#     stocks3 = 'SBIETFIT'
#     context = {
#         'nifty':stocks1,
#         'it':stocks2,
#         'sbi':stocks3,
#         'category':category
#     }
     
#     return render(request,'stocks.html',context)
 
def admincommoditiesdd(request):
    category = 'Commodities'
    com1 = 'SILVERBEES'
    com2 = 'GOLDBEES'
    com3 = 'EGOLD'
    
    context = {
        'silver':com1,
        'gold':com2,
        'egold':com3,
        'category':category
        
    }
    return render(request,'commodities.html',context)

def calculate_20dma(etf_name_list):
    # Get today's date
    today = date.today()

    # Initialize a dictionary to store 20DMA data for each ETF
    etf_data = {}
    etf_close_minus_20dma = {}
    etf_close_div_20dma = {}
    
    # Calculate 20-day moving average for each ETF
    for etf in etf_name_list:
        etf_name = etf.upper()
        # Get the model corresponding to the ETF name dynamically
        etf_model = globals()[etf_name]
        
        # Get 20-day data
        twenty_day_ago = today - timedelta(days=20)
        twenty_day_data = etf_model.objects.filter(date__gte=twenty_day_ago)
        
        # Calculate 20DMA
        twenty_day_sum = sum([price.close for price in twenty_day_data])
        twenty_day_avg = twenty_day_sum / len(twenty_day_data) if len(twenty_day_data) > 0 else 0

       

        close_minus_20dma = twenty_day_data.last().close - twenty_day_avg

        # Calculate close / 20DMA
        close_div_20dma = (twenty_day_avg / twenty_day_data.last().close) if twenty_day_avg != 0 else 0

        # Store 20DMA, close - 20DMA, and close / 20DMA ratio in respective dictionaries
        etf_data[etf] = twenty_day_avg
        etf_close_minus_20dma[etf] = close_minus_20dma
        etf_close_div_20dma[etf] = close_div_20dma

       

    return etf_data, etf_close_minus_20dma, etf_close_div_20dma


def calculate_50dma(etf_name_list):
    # Get today's date
    today = date.today()

    # Initialize dictionaries to store 50DMA data for each ETF
    etf_data_50dma = {}
    etf_close_minus_50dma = {}
    etf_close_div_50dma = {}
    
    # Calculate 50-day moving average for each ETF
    for etf in etf_name_list:
        etf_name = etf.upper()
        # Get the model corresponding to the ETF name dynamically
        etf_model = globals()[etf_name]
        
        # Get 50-day data
        fifty_day_ago = today - timedelta(days=50)
        fifty_day_data = etf_model.objects.filter(date__gte=fifty_day_ago)
        
        # Calculate 50DMA
        fifty_day_sum = sum([price.close for price in fifty_day_data])
        fifty_day_avg = fifty_day_sum / len(fifty_day_data) if len(fifty_day_data) > 0 else 0

        close_minus_50dma = fifty_day_data.last().close - fifty_day_avg

        # Calculate close / 50DMA
        close_div_50dma = (fifty_day_avg / fifty_day_data.last().close) if fifty_day_avg != 0 else 0

        # Store 50DMA, close - 50DMA, and close / 50DMA ratio in respective dictionaries
        etf_data_50dma[etf] = fifty_day_avg
        etf_close_minus_50dma[etf] = close_minus_50dma
        etf_close_div_50dma[etf] = close_div_50dma
        # print(etf_close_div_50dma)

    return etf_data_50dma, etf_close_minus_50dma, etf_close_div_50dma

def calculate_100dma(etf_name_list):
    # Get today's date
    today = date.today()

    # Initialize dictionaries to store 100DMA data for each ETF
    etf_data_100dma = {}
    etf_close_minus_100dma = {}
    etf_close_div_100dma = {}
    
    # Calculate 100-day moving average for each ETF
    for etf in etf_name_list:
        etf_name = etf.upper()
        # Get the model corresponding to the ETF name dynamically
        etf_model = globals()[etf_name]
        
        # Get 100-day data
        hundred_day_ago = today - timedelta(days=100)
        hundred_day_data = etf_model.objects.filter(date__gte=hundred_day_ago)
        
        # Calculate 100DMA
        hundred_day_sum = sum([price.close for price in hundred_day_data])
        hundred_day_avg = hundred_day_sum / len(hundred_day_data) if len(hundred_day_data) > 0 else 0

        close_minus_100dma = hundred_day_data.last().close - hundred_day_avg

        # Calculate close / 100DMA
        close_div_100dma = (hundred_day_avg / hundred_day_data.last().close) if hundred_day_avg != 0 else 0

        # Store 100DMA, close - 100DMA, and close / 100DMA ratio in respective dictionaries
        etf_data_100dma[etf] = hundred_day_avg
        etf_close_minus_100dma[etf] = close_minus_100dma
        etf_close_div_100dma[etf] = close_div_100dma

    return etf_data_100dma, etf_close_minus_100dma, etf_close_div_100dma



def calculate_percentage_diff(data):
    for i in range(1,len(data)):
            data[i].percent_diff = ((data[i].close - data[i-1].close) / data[i-1].close) * 100