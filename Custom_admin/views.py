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




# def commodities(request):
#     return render(request, 'commodities.html')

def admin_profile(request):
    return render(request, 'admin_profile.html')


def active_user(request):
    return render(request, 'active_user.html')


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

    
    # print(alldata)
    

    context = {
        'data':alldata,
        'etf_data':etf_data,
        'etf_close_minus_20dma': etf_close_minus_20dma,
        'etf_close_div_20dma': etf_close_div_20dma,
         'etf_data_50dma':etf_data_50dma,
        'etf_close_minus_50dma': etf_close_minus_50dma,
        'etf_close_div_50dma': etf_close_div_50dma,
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


def calculate_percentage_diff(data):
    for i in range(1,len(data)):
            data[i].percent_diff = ((data[i].close - data[i-1].close) / data[i-1].close) * 100