from django.shortcuts import render,redirect
from .models import RegisteredUser
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
import uuid
from django.conf import settings
from django.db.models import Avg
from datetime import timedelta, date


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


def user_profile(request):
    if request.user.is_authenticated:
        user = request.user.username
        data = RegisteredUser.objects.get(username = user)
        context = {
            'data':data
        }
    return render(request, 'user_profile.html', context)


def faq(request):
    return render(request, 'faq.html')


def Userbuy(request):
    if request.method == 'POST':
        # Retrieve form data from request.POST
        username  = request.POST.get('username')
        type = request.POST.get('type')
        etf = request.POST.get('ETF')
        close = request.POST.get('close')
        quant = request.POST.get('quant')
        
        
        data = AllETF.objects.all()
        asset = data.filter(assettype = type)
        closevalue = AllETF.objects.get(Etfnames = etf)
        
        
        context = {
            'data':data,
            'asset':asset,
            'closevalue':closevalue,
        }
    return render(request, 'user_buy.html',context)


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

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'useregold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'useregold.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'useregold.html', context)



def Abslnn50et(request):
        table_name = 'ABSLNN50ET'
        alldata = ABSLNN50ET_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userabslnn50et.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userabslnn50et.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userabslnn50et.html', context)

def Commoietf(request):
        table_name = 'COMMOIETF'
        alldata = COMMOIETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usercommoietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usercommoietf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usercommoietf.html', context)


def Cpseetf(request):
        table_name = 'CPSEETF'
        alldata = COMMOIETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usercpseetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usercpseetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usercpseetf.html', context)


def Dspitetf(request):
        table_name = 'DSPITETF'
        alldata = DSPITETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userdspitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userdspitetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userdspitetf.html', context)



def Dspq50etf(request):
        table_name = 'DSPQ50ETF'
        alldata = DSPQ50ETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userdspq50.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userdspq50.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userdspq50.html', context)

def Axistec(request):
        table_name = 'AXISTEC'
        alldata = AXISTECETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'useraxistec.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'useraxistec.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'useraxistec.html', context)


def Icicib22(request):
        table_name = 'ICICIB22'
        alldata = ICICIB22_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usericicib22.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usericicib22.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usericicib22.html', context)


def Infrabees(request):
        table_name = 'INFRABEES'
        alldata = INFRABEES_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userinfrabees.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userinfrabees.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userinfrabees.html', context)


def Iti(request):
        table_name = 'ITI'
        alldata = ITIETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'useriti.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'useriti.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'useriti.html', context)


def Kotak(request):
        table_name = 'KOTAK'
        alldata = KOTAKPSUBK_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userkotak.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userkotak.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userkotak.html', context)

def Mafang(request):
        table_name = 'MAFANG'
        alldata = MAFANG_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usermafang.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usermafang.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usermafang.html', context)


def Movalue(request):
        table_name = 'MOVALUE'
        alldata = MOVALUE_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usermovalue.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usermovalue.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usermovalue.html', context)


def Nifitetf(request):
        table_name = 'NIFITETF'
        alldata = NIFITETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usernifitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usernifitetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usernifitetf.html', context)

def Psubnk(request):
        table_name = 'PSUBNKIETF'
        alldata = PSUBNKIETF_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'userpsubnkietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'userpsubnkietf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'userpsubnkietf.html', context)




def Tech(request):
        table_name = 'TECH'
        alldata = TECH_NS.objects.all()

        if request.method == 'POST':
            start_date_str = request.POST.get('start_date')
            end_date_str = request.POST.get('end_date')
            print(start_date_str, end_date_str)

            if start_date_str and end_date_str:
                # Convert string dates to datetime objects
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

                queryset = alldata.filter(date__range=[start_date, end_date])
                print(start_date, end_date)
                context = {
                    'data': queryset,
                    'table_name':table_name
                }
                return render(request, 'usertechetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'usertechetf.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'usertechetf.html', context)


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
    
    # print(alldata)
    

    context = {
        'data':alldata,
        'etf_data':etf_data,
        'etf_close_minus_20dma': etf_close_minus_20dma,
        'etf_close_div_20dma': etf_close_div_20dma,
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




def calculate_percentage_diff(data):
    for i in range(1,len(data)):
            data[i].percent_diff = ((data[i].close - data[i-1].close) / data[i-1].close) * 100




# def calculate_etf_data(etf_name):
#     # Get today's date
#     today = date.today()
    

#     # Calculate 20-day moving average
#     twenty_day_ago = today - timedelta(days=20)
#     twenty_day_data = None
#     if etf_name == 'GOLDBEES_NS':
#         twenty_day_data = GOLDBEES_NS.objects.filter(date__gte=twenty_day_ago)
#     elif etf_name == 'NIFTYBEES_NS':
#         twenty_day_data = NIFTYBEES_NS.objects.filter(date__gte=twenty_day_ago)
#     elif etf_name == 'SILVERBEES_NS':
#         twenty_day_data = SILVERBEES_NS.objects.filter(date__gte=twenty_day_ago)
#     elif etf_name == 'ITBEES_NS':
#         twenty_day_data = ITBEES_NS.objects.filter(date__gte=twenty_day_ago)
#     elif etf_name == 'SBIETFIT_NS':
#         twenty_day_data = SBIETFIT_NS.objects.filter(date__gte=twenty_day_ago)
    
#     twenty_day_sum = sum(price.close for price in twenty_day_data)
#     twenty_day_avg = twenty_day_sum / len(twenty_day_data) if len(twenty_day_data) > 0 else 0

#     # Get today's close price
#     today_data = None
#     if etf_name == 'GOLDBEES_NS':
#         today_data = GOLDBEES_NS.objects.filter(date=today)
#     elif etf_name == 'NIFTYBEES_NS':
#         today_data = NIFTYBEES_NS.objects.filter(date=today)
#     elif etf_name == 'SILVERBEES_NS':
#         today_data = SILVERBEES_NS.objects.filter(date=today)
#     elif etf_name == 'ITBEES_NS':
#         today_data = ITBEES_NS.objects.filter(date=today)
#     elif etf_name == 'SBIETFIT_NS':
#         today_data = SBIETFIT_NS.objects.filter(date=today)

#     if today_data.exists():
#         today_close = today_data.first().close
#         cmp_vs_20dma = today_close - twenty_day_avg
#         if today_close > twenty_day_avg:
#             cmp_result = 'Above'
#         elif today_close < twenty_day_avg:
#             cmp_result = 'Below'
#         else:
#             cmp_result = 'Equal'
#         return {
#             '20dma': twenty_day_avg,
#             'close_vs_20dma': cmp_vs_20dma,
#             'cmp_vs_20dma': cmp_result
#         }
#     else:
#         return None








