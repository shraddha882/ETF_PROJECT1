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
from django.http import JsonResponse
from django.core.serializers import serialize
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def Userdashboard(request):
    if request.user.is_authenticated:
        user = request.user.username
        data = RegisteredUser.objects.get(username = user)
        context = {
            'data':data
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


def register(request):
     current_date = datetime.now().date()
     min_birth_date = (current_date - timedelta(days=365 * 18 + 4)).isoformat()
     if request.method == 'POST':
        # Retrieve form data from request.POST
        username  = request.POST.get('username')
        name = request.POST.get('Fname')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('dob')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Create a new User object and save it to the database
        # Check if an account with the same email already exists
        # current_date = datetime.now().date()
        birth_date = datetime.strptime(date_of_birth, '%Y-%m-%d').date() if date_of_birth else None

        # Regular expression to check for special characters and numbers in the full name
        if re.search(r'[!@#$%^&*()_+=[\]{};:"\\|,.<>/?\d]', str(name)):
            messages.error(request, 'Full Name cannot contain special characters or numbers.')
            
        # Limit the phone number to 10 digits
        elif not re.match(r'^\d{10}$', phone_number):
            messages.error(request, 'Phone number should be 10 digits long and contain only numbers.')
            
        # Check for other conditions
        elif birth_date and birth_date > current_date:
            messages.error(request, 'Invalid birth date. Please enter a valid date of birth.')
            
        # Check for 18+
        age = None if not birth_date else datetime.now().year - birth_date.year - ((datetime.now().month, datetime.now().day) < (birth_date.month, birth_date.day))
        if age is None or age < 18: messages.error(request, 'You must be 18 years old or older to register.')

            
            
        elif RegisteredUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use. Please choose a different one.')
        
        elif password == cpassword:
            email_token = str(uuid.uuid4())
           
            data = RegisteredUser.objects.create(username  = username,name=name, email=email, password=password, date_of_birth=date_of_birth, phone_number=phone_number, token=email_token)
            data.login_status = False
            data.save()
            
            # Create Wallet instance for the user
            wallet = Wallet.objects.create(user=data)
            wallet.save()
            

            user = User.objects.create_user(username=username,password=password)
            user.save() 
             
            print()
            
            # data = userdata.objects.create(user=user, username=username, Fname=name, email=email, password=password, email_token = email_token)
            send_email_after_registration(email,email_token)
            messages.success(request, 'Registration Link sent. Please click on link to verify your account')
            # return redirect('emailverified')
        
            # messages.success(request, 'Successfully registered')
            return redirect('Userlogin')
        
        else:
            messages.error(request, 'Passwords do not match. Registration failed.')

     context = { 
        'min_birth_date': min_birth_date
     }
     return render(request, 'Registration.html', context)
    

 


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



def Usertrans(request):
    user = request.user.username
    user_instance = RegisteredUser.objects.get(username=user)
    
    # Aggregate data for each distinct ETF name
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
    return render(request, 'user_transactions.html', context)

def userbuyhistory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            etf_name = data.get('ETFName')

            etfname = etf_name.upper()
            print(data)
            try:
                etf_model = globals()[etfname]
            except KeyError:
                return JsonResponse({'error': 'Invalid ETF name'}, status=400)
            
            
            detailed_data = UserBuyetf.objects.filter(Etf_purchased__Etfnames=etf_name).values('Date_time', 'Quantity', 'Cost', 'Purchase_close_value','trans_type')
            
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
# def Userbuy(request):
#     data = AllETF.objects.all()
#     closevalue = None
#     cost = None
    
#     if request.method == 'POST':
#         # Retrieve form data from request.POST
#         username = request.POST.get('username')
#         type = request.POST.get('type')
#         etf = request.POST.get('ETF')
#         quant = int(request.POST.get('quant'))
        
#         closevalue = AllETF.objects.get(Etfnames=etf).close  # Get the close value of the selected ETF
#         cost = closevalue * quant  # Calculate the cost
        
#     context = {   
#         'data': data,
#         'closevalue': closevalue,
#         'cost': cost,
#     }
    
#     return render(request, 'user_buy.html', context)

 
# def Userbuy(request):
#     data = AllETF.objects.all()
#     closevalue = None
#     cost = None
    
#     if request.method == 'POST':
#         username = request.user.username  
#         etf = request.POST.get('ETF')
#         # quant = int(request.POST.get('quant'))
        
#         # closevalue = AllETF.objects.get(Etfnames=etf).close  # Get the close value of the selected ETF
#         # cost = closevalue * Decimal(quant)  # Calculate the cost


#         quant = Decimal(request.POST.get('quant'))  # Convert to Decimal
        
#         closevalue = AllETF.objects.get(Etfnames=etf).close  # Get the close value of the selected ETF
#         closevalue = Decimal(closevalue)  # Convert to Decimal


        
#         cost = closevalue * quant  # Calculate the cost as Decimal
        
#         # Retrieve the wallet associated with the user
#         user_wallet = Wallet.objects.get(user__username=username)
        
#         # Check if the user has enough balance to make the purchase
#         if user_wallet.balance >= cost:
#             # Deduct the cost from the user's wallet balance
#             user_wallet.balance -= cost
#             user_wallet.save()  # Save the updated wallet balance
            
#             # Perform other actions related to buying the ETF
#             purchase = UserBuyetf.objects.create(
#                 Username=user_wallet.user,  # Assign the user to the ForeignKey field
#                 Etf_purchased=AllETF.objects.get(Etfnames=etf),  # Assign the purchased ETF
#                 Quantity=quant,
#                 Cost=cost
#             )
#             purchase.save()
            
#             # Redirect to a success page or display a success message
#             messages.success(request,"amount deducted successfully")
            
#             return redirect('UserBuy')  # Redirect to a success page
            
#         else:
#             # If the user doesn't have enough balance, display an error message
#             return render(request, 'insufficient_balance.html')
        
#     context = {   
#         'data': data,
#         'closevalue': closevalue,
#         'cost': cost,
#     }
    
#     return render(request, 'user_buy.html', context)

def Userbuy(request):
    data = AllETF.objects.all()
    closevalue = None
    cost = None
    username = request.user.username 
    
     # Retrieve distinct ETFs for the current user
    user_etfs = UserBuyetf.objects.filter(Username__username=username).select_related('Etf_purchased').values('Etf_purchased__Etfnames', 'Etf_purchased__close').distinct()
    print(user_etfs)
    
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')  # Add a hidden input field in each form to indicate its type
        
        if form_type == 'buy':  # Handle buy form submission
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
                
                # Redirect to a success page or display a success message
                messages.success(request, "Amount deducted successfully")
                return redirect('UserBuy')  # Redirect to a success page
                
            else:
                # If the user doesn't have enough balance, display an error message
                return render(request, 'insufficient_balance.html')
        
        elif form_type == 'sell':  # Handle sell form submission
            if request.method == 'POST':
                etf_id = request.POST.get('ETF')
                quantity = Decimal(request.POST.get('quant'))
                
                try:
                    # Retrieve the ETF object
                    etf = AllETF.objects.get(Etfnames=etf_id)
                    print("ETF object retrieved successfully:", etf)
                    
                    # Get the current close value of the ETF
                    current_close_value = Decimal(etf.close)
                    print("Current close value:", current_close_value)
                    
                    # Calculate total quantity of that ETF
                    buyetf = user_etfs.filter(Etf_purchased__Etfnames=etf_id)
                    total_cost = buyetf.aggregate(tquantity=Sum('Quantity'))['tquantity']
                    tquantity = total_cost if total_cost is not None else 0
                    print("Total quantity:", tquantity)
                    
                    # Get the purchase close value
                    purchase_close_value = etf.close
                    print("Purchase close value:", purchase_close_value)
                    
                    # Calculate the selling amount
                    selling_amount = current_close_value * quantity
                    print("Selling amount:", selling_amount)
                    
                    if quantity <= tquantity:
                        # Check if the user will make a profit by selling
                        if current_close_value >= purchase_close_value:
                            # Update user's wallet balance
                            user_wallet = Wallet.objects.get(user__username=username)
                            user_wallet.balance += selling_amount
                            user_wallet.save()
                            print("User's wallet balance updated successfully")
                            
                            # Add a new record for selling ETF to UserBuyetf table
                            UserBuyetf.objects.create(
                                Username=user_wallet.user,
                                Etf_purchased=etf,
                                Quantity=quantity,
                                Cost=selling_amount,
                                Purchase_close_value=purchase_close_value,
                                trans_type='SELL'
                            )
                            print("Record added to UserBuyetf table")
                            
                            # Redirect to a success page or display a success message
                            messages.success(request, "ETFs sold successfully")
                            return redirect('UserBuy')  # Redirect to a success page
                        else:
                            print("Current close value is lower than purchase close value. User will not make a profit.")
                            return render(request, 'user_buy.html', context)  # Render the user_buy.html template again with the current context
                    else:
                        messages.error(request, "Selected quantity exceeds the amount of ETFs you have.")
                        return redirect('UserBuy')
                except ObjectDoesNotExist:
                    messages.error(request, "Error: ETF data not found.")
                    return render(request, 'user_buy.html', context)  # Render the user_buy.html template again with the current context

                except Exception as e:
                    messages.error(request, f"Error: {str(e)}")
                    return render(request, 'user_buy.html', context)  # Render the user_buy.html template again with the current context

         # Clear messages from session
    storage = messages.get_messages(request)
    storage.used = True
        
    context = {   
        'data': data,
        'closevalue': closevalue,
        'cost': cost,
        'user_etfs': user_etfs,
    }
    
    return render(request, 'user_buy.html', context)

def usersell(request):
    username = request.user.username
    
    # Retrieve the user's purchased ETFs
    try:
        user_etfs = UserBuyetf.objects.filter(Username__username=username)
    except ObjectDoesNotExist:
        user_etfs = None
    
    if request.method == 'POST':
        etf_id = request.POST.get('etf_id')
        quantity = Decimal(request.POST.get('quant'))
        
        try:
            # Retrieve the ETF object
            etf = AllETF.objects.get(Etfnames=etf_id)
            
            # Get the current close value of the ETF
            current_close_value = Decimal(etf.close)
            
            # Get the purchase close value
            buyetf = user_etfs.get(Etf_purchased__Etfnames=etf_id)
            purchase_close_value = buyetf.Purchase_close_value
            
            # Calculate the selling amount
            selling_amount = current_close_value * quantity
            
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
                
                # Redirect to a success page or display a success message
                messages.success(request, "ETFs sold successfully")
                return redirect('sell_etf')  # Redirect to a success page
            else:
                return redirect('sell_etf')  # Redirect to the selling page again without an error message
        
        except ObjectDoesNotExist:
            messages.error(request, "Error: ETF data not found.")
            return redirect('sell_etf')
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('sell_etf')
    
    context = {   
        'user_etfs': user_etfs,
    }
    return render(request, 'sell_etf.html', context)
     

 


def error_404(request):
    return render(request, 'error_404.html')


def contact(request):
    return render(request, 'contact.html')


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
    

def NIFTYbees(request):
    table_name = 'NIFTYBEES'
    alldata = NIFTYBEES_NS.objects.all()
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
            return render(request, 'usernifty.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                'table_name':table_name,
                
            }
            return render(request, 'usernifty.html', context)

    # Default behavior: show all data
    context = {
               'data': data,
               'table_name':table_name,
               
               }
    return render(request, 'usernifty.html', context)


def GOLDbees(request):
        table_name = 'GOLDBEES'

        alldata = GOLDBEES_NS.objects.all()
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
                return render(request, 'usergold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name,
                    
                }
                return render(request, 'usergold.html', context)

        # Default behavior: show all data
        context = {
            'data': data,
            'table_name':table_name,
            

                   }
        return render(request, 'usergold.html', context)



def ITbees(request):
    table_name = 'ITBEES'
    alldata = ITBEES_NS.objects.all()
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
            return render(request, 'userit.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                'table_name':table_name,
                
            }
            return render(request, 'userit.html', context)

    # Default behavior: show all data
    context = {
        'data': data,
        'table_name':table_name,
        
               }
    return render(request, 'userit.html', context)


def SBIetfit(request):
    table_name = 'SBIETFIT'
    alldata = SBIETFIT_NS.objects.all()
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
            return render(request, 'usersbi.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                  'table_name':table_name
            }
            return render(request, 'usersbi.html', context)

    # Default behavior: show all data
    context = {'data': data,
               'table_name':table_name,
               
               }
    return render(request, 'usersbi.html', context)


def SILVERbees(request):
        table_name = 'SILVERBEES'
        alldata = SILVERBEES_NS.objects.all()
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
                return render(request, 'usersilver.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name,
                    
                }
                return render(request, 'usersilver.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name,
                   
                   
                   }
        
        return render(request, 'usersilver.html', context)




def Egold(request):
        table_name = 'EGOLD'
        alldata = EGOLD_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'useregold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'useregold.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'useregold.html', context)



def Abslnn50et(request):
        table_name = 'ABSLNN50ET'
        alldata = ABSLNN50ET_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'userabslnn50et.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userabslnn50et.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userabslnn50et.html', context)

def Commoietf(request):
        table_name = 'COMMOIETF'
        alldata = COMMOIETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usercommoietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usercommoietf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usercommoietf.html', context)


def Cpseetf(request):
        table_name = 'CPSEETF'
        alldata = COMMOIETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usercpseetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usercpseetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usercpseetf.html', context)


def Dspitetf(request):
        table_name = 'DSPITETF'
        alldata = DSPITETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'userdspitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userdspitetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userdspitetf.html', context)



def Dspq50etf(request):
        table_name = 'DSPQ50ETF'
        alldata = DSPQ50ETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'userdspq50.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userdspq50.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userdspq50.html', context)

def Axistec(request):
        table_name = 'AXISTEC'
        alldata = AXISTECETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'useraxistec.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'useraxistec.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'useraxistec.html', context)


def Icicib22(request):
        table_name = 'ICICIB22'
        alldata = ICICIB22_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usericicib22.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usericicib22.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usericicib22.html', context)


def Infrabees(request):
        table_name = 'INFRABEES'
        alldata = INFRABEES_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'userinfrabees.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userinfrabees.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userinfrabees.html', context)


def Iti(request):
        table_name = 'ITI'
        alldata = ITIETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'useriti.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'useriti.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'useriti.html', context)


def Kotak(request):
        table_name = 'KOTAK'
        alldata = KOTAKPSUBK_NS.objects.all()
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

                data = paginator.page(1)  # Reset to first page after filtering
                data = list(queryset)
                calculate_percentage_diff(data)
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userkotak.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userkotak.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userkotak.html', context)

def Mafang(request):
        table_name = 'MAFANG'
        alldata = MAFANG_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usermafang.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usermafang.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usermafang.html', context)


def Movalue(request):
        table_name = 'MOVALUE'
        alldata = MOVALUE_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usermovalue.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usermovalue.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usermovalue.html', context)


def Nifitetf(request):
        table_name = 'NIFITETF'
        alldata = NIFITETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'usernifitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usernifitetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'usernifitetf.html', context)

def Psubnk(request):
        table_name = 'PSUBNKIETF'
        alldata = PSUBNKIETF_NS.objects.all()
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
                    'table_name':table_name
                }
                return render(request, 'userpsubnkietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'userpsubnkietf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'userpsubnkietf.html', context)




def Tech(request):
        table_name = 'TECH'
        alldata = TECH_NS.objects.all()
        
        data = list(alldata)
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
                    'table_name':table_name
                }
                return render(request, 'usertechetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'usertechetf.html', context)

        # Default behavior: show all data
        context = {'data':data,
                   'table_name':table_name
                   }
        return render(request, 'usertechetf.html', context)
# def Tech(request):
#     table_name = 'TECH'
#     alldata = TECH_NS.objects.all()
#     data = list(alldata)
     

#     # Paginate your data
#     paginator = Paginator(alldata, 10)  # Show 10 records per page
#     page = request.GET.get('page')
    
#     try:
#         data = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         data = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         data = paginator.page(paginator.num_pages)

#     if request.method == 'POST':
#         start_date_str = request.POST.get('start_date')
#         end_date_str = request.POST.get('end_date')

#         if start_date_str and end_date_str:
#             # Convert string dates to datetime objects
#             start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
#             end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

#             queryset = alldata.filter(date__range=[start_date, end_date])
#             data = paginator.page(1)  # Reset to first page after filtering
#             data = list(queryset)
#             calculate_percentage_diff(data)
#             return render(request, 'usertechetf.html', {'data': data, 'table_name': table_name})
#         else:
#             # If start_date or end_date is not provided, show all data
#             return render(request, 'usertechetf.html', {'data': data, 'table_name': table_name})

#     # Default behavior: show all data
#     return render(request, 'usertechetf.html', {'data': data, 'table_name': table_name})


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
    etf_data_50dma, etf_close_minus_50dma, etf_close_div_50dma = calculate_50dma(etf_name_list)
    etf_data_100dma, etf_close_minus_100dma, etf_close_div_100dma = calculate_100dma(etf_name_list)
    
    # print(alldata)
    

    context = {
        'data':alldata,
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
        'category':category

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
    

 





