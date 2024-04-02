from django.shortcuts import render,redirect
from .models import RegisteredUser,Wallet
from django.contrib import messages
from django.contrib.auth.models import User
from Custom_admin.models import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import login as loginuser, authenticate, logout
import re
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
import uuid, pytz
import json, datetime
from django.conf import settings
from django.db.models import Avg
from django.db.models import Sum, Avg, Max, Case, When, F,FloatField, Value
from django.db.models.functions import Coalesce, Cast
from datetime import timedelta, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from decimal import Decimal
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseServerError
from django.core.serializers import serialize
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def Userdashboard(request):
    
    user = request.user.username
    data = RegisteredUser.objects.get(username = user)
    if request.method == 'POST':
        subs = request.POST.get('subs')
        data.sub_status = subs
        data.save()
    context = {
        'data':data,
        'user':user
        }

    return render(request,'UserDashboard.html', context)


def user_login(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        username  = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
                    if user.is_superuser:
                        loginuser(request, user)
                        return redirect('admindashboard')
                    else:
                        try:
                            profile = RegisteredUser.objects.get(username=username)

                            if profile.is_verified:
                                if profile.login_status:
                                    loginuser(request,user)
                                    return redirect('UserDashboard')
                                else :
                                    messages.error(request,'Please wait for admin to verify your request.')
                            elif not profile.is_verified:
                                messages.error(request, 'Please check your email for the verification link.')
       
                        except RegisteredUser.DoesNotExist:
                            messages.error(request, 'Details not found. Please register.')
                            return render(request, 'login.html')
        else:
            messages.error(request, 'Details not found. Please register.')                        
                        
    return render(request, 'login.html')

def send_email_after_registration(email, token):
    # send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None, auth_password=None, connection=None, html_message=None)
    subject ="Verify Email"
    message = f"Hi click on the link to verify your account http://127.0.0.1:8000/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list =[email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)


# def register(request):
#     current_date = datetime.datetime.now().date()
#     min_birth_date = (current_date - timedelta(days=365 * 18 + 4)).isoformat()

#     if request.method == 'POST':
#         # Retrieve form data from request.POST
#         username = request.POST.get('username')
#         name = request.POST.get('Fname')
#         email = request.POST.get('email')
#         date_of_birth = request.POST.get('dob')
#         phone_number = request.POST.get('phone')
#         password = request.POST.get('password')
#         cpassword = request.POST.get('cpassword')

#         # Regular expression to check for special characters and numbers in the full name
#         if re.search(r'[!@#$%^&*()_+=[\]{};:"\\|,.<>/?\d]', str(name)):
#             messages.error(request, 'Full Name cannot contain special characters or numbers.')
#         # Limit the phone number to 10 digits
#         elif not re.match(r'^\d{10}$', phone_number):
#             messages.error(request, 'Phone number should be 10 digits long and contain only numbers.')
#         else:
#             birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None

#             if birth_date and birth_date > current_date:
#                 messages.error(request, 'Invalid birth date. Please enter a valid date of birth.')
#             elif RegisteredUser.objects.filter(email=email).exists():
#                 messages.error(request, 'Email is already in use. Please choose a different one.')
#             elif password != cpassword:
#                 messages.error(request, 'Passwords do not match. Registration failed.')
#             else:
#                 email_token = str(uuid.uuid4())

#                 data = RegisteredUser.objects.create(username=username, name=name, email=email, password=password,
#                                                       date_of_birth=date_of_birth, phone_number=phone_number,
#                                                       token=email_token)
#                 data.login_status = False
#                 data.sub_status = 'Unsubscribed'
#                 data.save()

#                 user = User.objects.create_user(username=username, password=password)
#                 user.save()

#                 wallet = Wallet.objects.create(user = data)
#                 wallet.save()
                
#                 send_email_after_registration(email, email_token)
#                 messages.success(request, 'Registration Link sent. Please click on link to verify your account')
#                 return redirect('Userlogin')

#     context = {
#         'min_birth_date': min_birth_date
#     }
#     return render(request, 'Registration.html', context)  

def register(request):
    current_date = datetime.datetime.now().date()
    min_birth_date = (current_date - timedelta(days=365 * 18 + 4)).isoformat()

    if request.method == 'POST':
        # Retrieve form data from request.POST
        username = request.POST.get('username')
        name = request.POST.get('Fname')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('dob')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Regular expression to check for special characters and numbers in the full name
        if re.search(r'[!@#$%^&*()_+=[\]{};:"\\|,.<>/?\d]', str(name)):
            messages.error(request, 'Full Name cannot contain special characters or numbers.')
        # Limit the phone number to 10 digits
        elif not re.match(r'^\d{10}$', phone_number):
            messages.error(request, 'Phone number should be 10 digits long and contain only numbers.')
        # Check if passwords match
        elif password != cpassword:
            messages.error(request, 'Passwords do not match. Registration failed.')
        # Check if password is strong enough
        elif not is_strong_password(password):
            messages.error(request, 'Password is not strong. Please use a stronger password.')
        else:
            birth_date = datetime.datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None

            if birth_date and birth_date > current_date:
                messages.error(request, 'Invalid birth date. Please enter a valid date of birth.')
            elif RegisteredUser.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use. Please choose a different one.')
            else:
                email_token = str(uuid.uuid4())

                data = RegisteredUser.objects.create(username=username, name=name, email=email, password=password,
                                                      date_of_birth=date_of_birth, phone_number=phone_number,
                                                      token=email_token)
                data.login_status = False
                data.save()

                user = User.objects.create_user(username=username, password=password)
                user.save()

                wallet = Wallet.objects.create(user = data)
                wallet.sub_status = 'Unsubscribed'
                wallet.period = '1 month'
                wallet.save()
                
                send_email_after_registration(email, email_token)
                messages.success(request, 'Registration Link sent. Please click on link to verify your account')
                return redirect('Userlogin')

    context = {
        'min_birth_date': min_birth_date
    }
    return render(request, 'Registration.html', context)
def is_strong_password(password):
    # Define your password strength criteria here
    # For example, you can check length, presence of uppercase letters, lowercase letters, numbers, and special characters
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password) and any(c in '!@#$%^&*()-_+=' for c in password)

def accout_verify(request,token):
    pf = RegisteredUser.objects.filter(token=token).first()
    pf.is_verified = True
    pf.save()
                 
    # pf.is_active = False
    return render (request, 'login.html')


# def user_profile(request):
#     if request.user.is_authenticated:
#         user = request.user.username
         
#         data = RegisteredUser.objects.get(username = user)
#         context = {
#             'data':data,
            
#         }
#     return render(request, 'user_profile.html', context)
 
 
def user_profile(request):
    context = {}
    if request.user.is_authenticated:
        user = request.user.username
         
        data = RegisteredUser.objects.get(username=user)
        
        try:
            wallet = Wallet.objects.get(user=data)
        except Wallet.DoesNotExist:
            wallet = None
        
        context = {
            'data': data,
            'wallet': wallet
        }
    return render(request, 'user_profile.html', context)



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

def Usertrans(request):
    if request.method == 'GET':
        try:
            user_instance = RegisteredUser.objects.get(username=request.user.username)
        except RegisteredUser.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        
        aggregated_data_buy = aggregate_buy_transactions(user_instance)
        modified_data_buy = modify_data(aggregated_data_buy)

        aggregated_data_sell = aggregate_sell_transactions(user_instance)
        modified_data_sell = modify_data(aggregated_data_sell)
    
        aggregated_data_all = aggregate_all_transactions(user_instance)
        modified_data_all = modify_data(aggregated_data_all)
        
        context = {
            'data_all': modified_data_all,
            'data_buy': modified_data_buy,
            'data_sell': modified_data_sell,
            
            }

        return render(request, 'user_transactions.html', context)

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

def subs(request):
    if request.method == 'POST':
        # Load the request body as JSON
        data = json.loads(request.body)
        user = request.user.username
        # Extract subscriptionType and timePeriod from the JSON data
        subscription_type = data.get('subscriptionType')
        time_period = data.get('timePeriod')
        print(subscription_type, time_period)
        
        reg = RegisteredUser.objects.get(username=user)
        wallet = Wallet.objects.get(user=reg)
        
        # Use the start_date to calculate the end_date
        start_date = timezone.now()
        wallet.start_date = start_date
        end_date = None  # Initialize end_date variable
        
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
        
        # Update subscription status, period, end_date, and remaining_days
        wallet.sub_status = subscription_type
        wallet.period = time_period
        wallet.end_date = end_date
        wallet.remaining_days = remaining_days
        
        # Save the changes to the wallet
        wallet.save()
        
        # Check if current date is equal to end date
        if end_date and timezone.now().date() == end_date.date():
            # Revert subscription status and period to default values
            wallet.sub_status = 'Unsubscribed'
            wallet.period = '1 month'
            wallet.end_date = None
            wallet.remaining_days = None
            # Other fields can be set to None or default values as needed
            
            # Save the changes to the wallet
            wallet.save()
        
        # Return a JSON response indicating success
        return JsonResponse({'message': 'Subscription updated successfully'})

def userbuydetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = request.user.username

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

def userselldetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = request.user.username
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

def useralldetails(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')
            username = request.user.username
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

def Userbuy(request):
    data = list(AllETF.objects.values_list('Etfnames', flat=True))
    closevalue = None
    cost = None
    username = request.user.username 
    
    # Retrieve distinct ETFs for the current user
    user_etfs = UserBuyetf.objects.filter(Username__username=username).select_related('Etf_purchased').values('Etf_purchased__Etfnames', 'Etf_purchased__close').distinct()
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Add a hidden input field in each form to indicate its type
        
        if form_type == 'get_close_value':
            selected_etf = request.POST.get('selected_etf')
            try:
                # Retrieve the selected ETF object and its close value
                selected_etf_obj = get_object_or_404(AllETF, Etfnames=selected_etf)
                close_value = selected_etf_obj.close
                return JsonResponse({'success': True, 'closevalue': close_value})
            except AllETF.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Selected ETF not found'}, status=400)
        elif form_type == 'buy':  # Handle buy form submission
            etf = request.POST.get('ETF')
            
            # Retrieve the selected ETF object and its close value in one query
            selected_etf = get_object_or_404(AllETF, Etfnames=etf)
            closevalue = Decimal(selected_etf.close)
            
            quant = Decimal(request.POST.get('quant'))  # Convert to Decimal
            cost = closevalue * quant  # Calculate the cost as Decimal
            
            # Retrieve the wallet associated with the user
            user_wallet = Wallet.objects.get(user__username=username)
            
            # Check if the user has enough balance to make the purchase
            if user_wallet.balance >= cost:
                # Deduct the cost from the user's wallet balance
                user_wallet.balance -= cost
                user_wallet.save()  # Save the updated wallet balance
                
                # Perform other actions related to buying the ETF
                purchase = UserBuyetf.objects.create(
                    Username=user_wallet.user,  # Assign the user to the ForeignKey field
                    Etf_purchased=selected_etf,  # Assign the purchased ETF
                    Quantity=quant,
                    Cost=cost,
                    Purchase_close_value=closevalue,  # Assign the purchase close value
                    trans_type='BUY'
                )
                
                messages.success(request, "ETF Purchased successfully")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the same page                
            else:
                return JsonResponse({'success': False, 'message': 'You do not have enough balance to buy'})
        
        elif form_type == 'sell':  # Handle sell form submission
            etf_id = request.POST.get('ETF')
            quantity = Decimal(request.POST.get('quant'))
            print(etf_id)
            
             # Retrieve the ETF object
            etf = AllETF.objects.get(Etfnames=etf_id)
            
            # Get the current close value of the ETF
            current_close_value = Decimal(etf.close)
            
            # Calculate total quantity of that ETF
            buyetf = user_etfs.filter(Etf_purchased__Etfnames=etf_id)
            total_cost = buyetf.aggregate(tquantity=Sum('Quantity'))['tquantity']
            tquantity = total_cost if total_cost is not None else 0
            
            # Get the purchase close value
            purchase_close_value = etf.close
            
            # Calculate the selling amount
            selling_amount = current_close_value * quantity
            
            if quantity <= tquantity:
                # Check if the user will make a profit by selling
                if current_close_value >= purchase_close_value:
                    # Update user's wallet balance
                    user_wallet = Wallet.objects.get(user__username=username)
                    user_wallet.balance += selling_amount
                    user_wallet.save()
                    
                    # Add a new record for selling ETF to UserBuyetf table
                    UserBuyetf.objects.create(
                        Username=user_wallet.user,
                        Etf_purchased=etf,
                        Quantity=quantity,
                        Cost=selling_amount,
                        Purchase_close_value=purchase_close_value,
                        trans_type='SELL'
                    )
                    
                    messages.error(request, "ETF sold successfully")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Redirect back to the same page
                else:
                    return JsonResponse({'success': False, 'message': 'Current close value is lower than purchase close value. You will not make a profit.'})
            else:
                return JsonResponse({'success': False, 'message': 'Selected quantity exceeds the amount of ETFs you have.'})
                
    # If it's not a POST request, return the context data
    
    context = {   
        'data': data,
        'closevalue': closevalue,
        'cost': cost,
        'user_etfs': list(user_etfs),
    }
    
    return JsonResponse(context)
    

def error_404(request):
    return render(request, 'error_404.html')


def contact(request):
    return render(request, 'contact.html')

def usersell(request):
    return render(request,'sell_etf.html')
# def userstocks(request):
#     table_name = 'NIFTYBEES'
#     alldata = NIFTYBEES_NS.objects.all()

#     if request.method == 'POST':
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')
#         print(start_date_str, end_date_str)

#         if start_date_str and end_date_str:
#             # Convert string dates to datetime objects
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#             queryset = alldata.filter(date__range=[start_date, end_date])
#             print(start_date, end_date)
#             context = {
#                 'data': queryset
#             }
#             return render(request, 'userstocks.html', context)
#         else:
#             # If start_date or end_date is not provided, show all data
#             context = {
#                 'data': alldata
#             }
#             return render(request, 'userstocks.html', context)

#     # Default behavior: show all data
#     context = {'data': alldata,
#                'table_name':table_name
#                }
#     return render(request, 'userstocks.html', context)
     

# def usercommodities(request):
#         table_name = 'SILVERBEES'
#         alldata = SILVERBEES_NS.objects.all()

#         if request.method == 'POST':
#             start_date_str = request.POST.get('start_date')
#             end_date_str = request.POST.get('end_date')
#             print(start_date_str, end_date_str)

#             if start_date_str and end_date_str:
#                 # Convert string dates to datetime objects
#                 start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#                 end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#                 queryset = alldata.filter(date__range=[start_date, end_date])
#                 print(start_date, end_date)
#                 context = {
#                     'data': queryset
#                 }
#                 return render(request, 'usercommodities.html', context)
#             else:
#                 # If start_date or end_date is not provided, show all data
#                 context = {
#                     'data': alldata
#                 }
#                 return render(request, 'usercommodities.html', context)

#         # Default behavior: show all data
#         context = {'data': alldata}
#         return render(request, 'usercommodities.html', context)
    

def etftables(request,table):
    
    table_name = table.upper()
    model=globals()[table_name]
    alldata = model.objects.all()
    data = list(alldata)
    calculate_percentage_diff(data)
    paginator = Paginator(alldata, 10)  # Show 10 records per page
    page = request.GET.get('page')
            
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
                # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        print(start_date_str, end_date_str)

        if start_date_str and end_date_str:
            # Convert string dates to datetime objects
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

            queryset = alldata.filter(date__range=[start_date, end_date])
            data = paginator.page(1) 
            data = list(queryset)
            calculate_percentage_diff(data)           
            print(start_date, end_date)
            context = {
                'data': data,
                'table_name':table_name,
                
            }
            return render(request, 'useretftables.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                'table_name':table_name,
                
            }
            return render(request, 'useretftables.html', context)

    # Default behavior: show all data
    context = {
               'data': data,
               'table_name':table_name,
               
               }
    return render(request, 'useretftables.html', context)



def Logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('Userlogin')

# def userstocksdd(request):
     
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
     
#     return render(request,'userstocks.html',context)
 
def usercommoditiesdd(request):
    category = 'Commodities'
    com1 = 'SILVERBEES'
    com2 = 'GOLDBEES'
    com3='EGOLD'
    
    context = {
        'silver':com1,
        'gold':com2,
        'egold':com3,
        'category':category
        
    }
    return render(request,'usercommodities.html',context)


def userstocks(request):
    user=request.user.username
    user_instance = RegisteredUser.objects.get(username=user)
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
    data = list(alldata)
    # etf_names = AllETF.objects.all().values('Etfnames' ,flat=True)
    # etf_name_list = list(etf_names.values())
    # print(etf_name_list)
    paginator = Paginator(alldata, 10)  # Show 10 records per page
    page = request.GET.get('page')
        
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        data = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)
    etf_names = AllETF.objects.all().values_list('Etfnames', flat=True)
    etf_name_list = list(etf_names)
    

    etf_data, etf_close_minus_20dma, etf_close_div_20dma = calculate_20dma(etf_name_list)
    etf_data_50dma, etf_close_minus_50dma, etf_close_div_50dma = calculate_50dma(etf_name_list)
    etf_data_100dma, etf_close_minus_100dma, etf_close_div_100dma = calculate_100dma(etf_name_list)
    
    # print(alldata)
    

    context = {
        'data':data,
        'etf_data':etf_data,
        'etf_close_minus_20dma': etf_close_minus_20dma,
        'etf_close_div_20dma': etf_close_div_20dma,
        'etf_data_50dma': etf_data_50dma,
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
        'category':category,
        'user':user_instance

    }
    return render(request, 'userstocks.html',context)

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
        print(etf_name)
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




from datetime import date, timedelta

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




# def calculate_etf_data(etf_name):
#     # Get today's date
#     today = date.today()
    

 





