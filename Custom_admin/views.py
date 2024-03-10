from django.shortcuts import render
from django.shortcuts import render, redirect ,HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as loginuser, authenticate, logout ,login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib import messages
from registeredUser.models import RegisteredUser
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


def admindashboard(request):
        return render(request, 'admindashboard.html')
        

def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('Userlogin')





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
        return render(request, 'users_data.html', {'users': users})
    

# @login_required
def Approve(request,username):
    update=RegisteredUser.objects.get(username=username)
    user=User.objects.get(username=username)
    if user is not None:
        update.login_status=True
        update.save()
        messages.success(request, f'{username} is now allowed to Login')  
    else:
        update.delete()
    return redirect('users_data')

# @login_required
def Decline(request,username):
    update=RegisteredUser.objects.get(username=username)
    user=User.objects.get(username=username)
    if user is not None:    
        update.login_status=False
        update.save()
        messages.error(request, f'{username} is not allowed to Login')
    else:
        update.delete()
    return redirect('users_data')

def active_user(request):
    active_registered_users = RegisteredUser.objects.filter(login_status=True,is_verified=True)
    #user = request.user.username
    # user_instance = None
    # if request.method == 'POST':
    #      data = json.loads(request.body)
    #      username = data.get('username')
    #      user_instance = RegisteredUser.objects.get(username=username)
    aggregated_data={}
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_instance = data.get('username')
            print(user_instance)
            transaction_type = data.get('transactionType')
             
              # Extract selected transaction type from request
            if transaction_type == 'BUY':
                # Aggregate data for BUY transactions
                aggregated_data = (
                    UserBuyetf.objects.filter(Username=user_instance, trans_type='BUY')
                    .values('Etf_purchased__Etfnames')
                    .annotate(
                        total_quantity=Sum('Quantity'),
                        total_cost=Sum('Cost')
                    )
                )
                  # Fetch current price for each ETF
                current_prices = {}
                for entry in aggregated_data:
                    etfname = entry['Etf_purchased__Etfnames']
                    try:
                        current_prices[etfname] = (AllETF.objects.get(Etfnames=etfname).close)
                    except AllETF.DoesNotExist:
                        # Handle the case where the object is not found
                        # For example, set the price to 0 or handle it according to your logic
                        current_prices[etfname] = 0.0  # Set the price to 0

                
                # Convert datetime fields to Indian Standard Time (IST) and create a new list of modified entries
                modified_data = []
                for entry in aggregated_data:
                    entry['mod_date'] = entry['latest_date'].date()
                    
                    # Calculate average cost
                    if entry['total_quantity'] != 0:
                        entry['mod_avg'] = entry['total_cost'] / entry['total_quantity']
                    else:
                        entry['mod_avg'] = 0.00
                    
                    entry['current_price'] = current_prices.get(entry['Etf_purchased__Etfnames'], 0)
                    
                    # Calculate percent difference without rounding off
                    if entry['mod_avg'] != 0:  # Ensure no division by zero
                        percent_diff = (entry['current_price'] - entry['mod_avg']) / entry['mod_avg'] * 100
                    else:
                        percent_diff = float('0') if entry['current_price'] > 0 else float('-inf')
                    entry['percent_diff'] = percent_diff
                    
                    
                    
                    modified_data.append(entry)  # Add the modified entry to the new list
                #     print(modified_data)
                context = {
                    'data': modified_data  # Pass the modified data to the template context
                }

                return JsonResponse(context)
            elif transaction_type == 'SELL':
                # Aggregate data for SELL transactions
                aggregated_data = (
                    UserBuyetf.objects.filter(Username=user_instance, trans_type='SELL')
                    .values('Etf_purchased__Etfnames')
                    .annotate(
                        total_quantity=Sum('Quantity'),
                        total_cost=Sum('Cost')
                    )
                )
                  # Fetch current price for each ETF
                current_prices = {}
                for entry in aggregated_data:
                    etfname = entry['Etf_purchased__Etfnames']
                    try:
                        current_prices[etfname] = (AllETF.objects.get(Etfnames=etfname).close)
                    except AllETF.DoesNotExist:
                        # Handle the case where the object is not found
                        # For example, set the price to 0 or handle it according to your logic
                        current_prices[etfname] = 0.0  # Set the price to 0

                
                # Convert datetime fields to Indian Standard Time (IST) and create a new list of modified entries
                modified_data = []
                for entry in aggregated_data:
                    entry['mod_date'] = entry['latest_date'].date()
                    
                    # Calculate average cost
                    if entry['total_quantity'] != 0:
                        entry['mod_avg'] = entry['total_cost'] / entry['total_quantity']
                    else:
                        entry['mod_avg'] = 0.00
                    
                    entry['current_price'] = current_prices.get(entry['Etf_purchased__Etfnames'], 0)
                    
                    # Calculate percent difference without rounding off
                    if entry['mod_avg'] != 0:  # Ensure no division by zero
                        percent_diff = (entry['current_price'] - entry['mod_avg']) / entry['mod_avg'] * 100
                    else:
                        percent_diff = float('0') if entry['current_price'] > 0 else float('-inf')
                    entry['percent_diff'] = percent_diff
                    
                    
                    
                    modified_data.append(entry)  # Add the modified entry to the new list
                #     print(modified_data)
                context = {
                    'data': modified_data  # Pass the modified data to the template context
                }

                return JsonResponse(context)
            else:
                # Handle if trans_type is not specified, default to 'BUY'
                    aggregated_data = (
                        UserBuyetf.objects.filter(Username=user_instance)
                        .values('Etf_purchased__Etfnames')
                        .annotate(
                            latest_date=Max('Date_time'),
                            totalquantity=Sum(
                                Case(
                                    When(trans_type='BUY', then=F('Quantity')),
                                    When(trans_type='SELL', then=F('Quantity') * -1),  # Negate quantity for sells
                                    default=0,
                                    output_field=FloatField()
                                )
                            ),
                            totalcost=Sum(
                                Case(
                                    When(trans_type='BUY', then=F('Cost')),
                                    When(trans_type='SELL', then=F('Cost') * -1),  # Negate total amount for sells
                                    default=0,
                                    output_field=FloatField()
                                )
                            )
                        )
                    )
                      # Fetch current price for each ETF
                    current_prices = {}
                    for entry in aggregated_data:
                        etfname = entry['Etf_purchased__Etfnames']
                        try:
                            current_prices[etfname] = (AllETF.objects.get(Etfnames=etfname).close)
                        except AllETF.DoesNotExist:
                            # Handle the case where the object is not found
                            # For example, set the price to 0 or handle it according to your logic
                            current_prices[etfname] = 0.0  # Set the price to 0

                    
                    # Convert datetime fields to Indian Standard Time (IST) and create a new list of modified entries
                    modified_data = []
                    for entry in aggregated_data:
                        entry['moddate'] = entry['latest_date'].date()
                        entry['Etfnames'] = entry['Etf_purchased__Etfnames']
                        
                        # Calculate average cost
                        if entry['totalquantity'] != 0:
                            entry['modavg'] = entry['totalcost'] / entry['totalquantity']
                        else:
                            entry['modavg'] = 0.00
                        
                        entry['currentprice'] = current_prices.get(entry['Etf_purchased__Etfnames'], 0)
                        
                        # Calculate percent difference without rounding off
                        if entry['modavg'] != 0:  # Ensure no division by zero
                            percent_diff = (entry['currentprice'] - entry['modavg']) / entry['modavg'] * 100
                        else:
                            percent_diff = float('0') if entry['currentprice'] > 0 else float('-inf')
                        entry['percentdiff'] = percent_diff
                        
                        
                        
                        modified_data.append(entry)  # Add the modified entry to the new list
                    #     print(modified_data)
                    context = {
                        'data': modified_data  # Pass the modified data to the template context
                    }

                    return JsonResponse(context)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        if request.method == 'POST':
        # Handle if trans_type is not specified, default to 'BUY'
            data = json.loads(request.body)
            user_instance = data.get('username')
            print(user_instance)
            aggregated_data = (
                UserBuyetf.objects.filter(Username=user_instance)
                .values('Etf_purchased__Etfnames')
                .annotate(
                    latest_date=Max('Date_time'),
                    total_quantity=Sum(
                        Case(
                            When(trans_type='BUY', then=F('Quantity')),
                            When(trans_type='SELL', then=F('Quantity') * -1),  # Negate quantity for sells
                            default=0,
                            output_field=FloatField()
                        )
                    ),
                    total_cost=Sum(
                        Case(
                            When(trans_type='BUY', then=F('Cost')),
                            When(trans_type='SELL', then=F('Cost') * -1),  # Negate total amount for sells
                            default=0,
                            output_field=FloatField()
                        )
                    )
                )
            )
            print(aggregated_data)
            # Fetch current price for each ETF
           # Fetch current price for each ETF
            current_prices = {}
            for entry in aggregated_data:
                etfname = entry['Etf_purchased__Etfnames']
                try:
                    current_prices[etfname] = (AllETF.objects.get(Etfnames=etfname).close)
                except AllETF.DoesNotExist:
                    # Handle the case where the object is not found
                    # For example, set the price to 0 or handle it according to your logic
                    current_prices[etfname] = 0.0  # Set the price to 0

            
            # Convert datetime fields to Indian Standard Time (IST) and create a new list of modified entries
            modified_data = []
            for entry in aggregated_data:
                entry['mod_date'] = entry['latest_date'].date()
                entry['Etfnames'] = entry['Etf_purchased__Etfnames'].upper()
                print(entry['Etfnames'])
                
                # Calculate average cost
                if entry['total_quantity'] != 0:
                    entry['mod_avg'] = entry['total_cost'] / entry['total_quantity']
                else:
                    entry['mod_avg'] = 0.00
                
                entry['current_price'] = current_prices.get(entry['Etf_purchased__Etfnames'], 0)
                print(entry['current_price'])
                # Calculate percent difference without rounding off
                if entry['mod_avg'] != 0:  # Ensure no division by zero
                    percent_diff = (entry['current_price'] - entry['mod_avg']) / entry['mod_avg'] * 100
                else:
                    percent_diff = float('0') if entry['current_price'] > 0 else float('-inf')
                entry['percent_diff'] = percent_diff
                entry['20dma'],entry['etf_close_minus_20dma'], entry['etf_close_div_20dma'] = calculate_20dma([entry['Etfnames']])
                entry['50dma'],entry['etf_close_minus_50dma'], entry['etf_close_div_50dma'] = calculate_50dma([entry['Etfnames']])
                entry['100dma'],entry['etf_close_minus_100dma'], entry['etf_close_div_100dma'] = calculate_100dma([entry['Etfnames']])
                # print(entry['20dma'])
                modified_data.append(entry)  # Add the modified entry to the new list
            #     print(modified_data)
            context = {
                'data': active_registered_users,
                'data1': modified_data  # Pass the modified data to the template context
            }
        context = {
                'data': active_registered_users,
                # 'data1': modified_data  # Pass the modified data to the template context
            }
    
    return render(request, 'active_user.html', context)

def deactivate_user(request):
    deactivate_registered_users = RegisteredUser.objects.filter(login_status=False)
    context ={
         'data': deactivate_registered_users
    }
    return render(request, 'deactivate_user.html', context)





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

def admin_profile(request):
    return render(request, 'admin_profile.html')


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
            return render(request, 'adminNifty.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                  'table_name':table_name,
                    'category':category
            }
            return render(request, 'adminNifty.html', context)

    # Default behavior: show all data
    context = {
                'data': alldata,
               'table_name':table_name,
                 'category':category
               
               }
    return render(request,'adminNifty.html',context)

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