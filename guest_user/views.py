from django.shortcuts import render,HttpResponseRedirect,redirect
from Custom_admin.models import *
from datetime import datetime,date
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request,'index.html')



def stocksIndex(request):
    table_name = 'NIFTYBEES'
    alldata = NIFTYBEES_NS.objects.all()

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
                'data': queryset
            }
            return render(request, 'stocksIndex.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata
            }
            return render(request, 'stocksIndex.html', context)

    # Default behavior: show all data
    context = {'data': alldata,
               'table_name':table_name
               }
    return render(request, 'stocksIndex.html', context)
     

def commoditiesIndex(request):
        table_name = 'SILVERBEES'
        alldata = SILVERBEES_NS.objects.all()

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
                    'data': queryset
                }
                return render(request, 'commoditiesIndex.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata
                }
                return render(request, 'commoditiesIndex.html', context)

        # Default behavior: show all data
        context = {'data': alldata}
        return render(request, 'commoditiesIndex.html', context)
    

def niftybees(request):
    table_name = 'NIFTYBEES'
    alldata = NIFTYBEES_NS.objects.all()

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
            return render(request, 'nifty.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                  'table_name':table_name
            }
            return render(request, 'nifty.html', context)

    # Default behavior: show all data
    context = {
                'data': alldata,
               'table_name':table_name
               
               }
    return render(request, 'nifty.html', context)


def goldbees(request):
        table_name = 'GOLDBEES'

        alldata = GOLDBEES_NS.objects.all()

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
                return render(request, 'gold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                     'table_name':table_name
                }
                return render(request, 'gold.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   
                   'table_name':table_name
                   }
        return render(request, 'gold.html', context)



def itbees(request):
    table_name = 'ITBEES'
    alldata = ITBEES_NS.objects.all()

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
            return render(request, 'it.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                'table_name':table_name
            }
            return render(request, 'it.html', context)

    # Default behavior: show all data
    context = {
        'data': alldata,
        'table_name':table_name
               }
    return render(request, 'it.html', context)


def sbietfit(request):
    table_name = 'SBIETFIT'
    alldata = SBIETFIT_NS.objects.all()

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
            return render(request, 'sbi.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': alldata,
                 'table_name':table_name
            }
            return render(request, 'sbi.html', context)

    # Default behavior: show all data
    context = {'data': alldata,
               'table_name':table_name
               }
    return render(request, 'sbi.html', context)


def silverbees(request):
        table_name = 'SILVERBEES'
        alldata = SILVERBEES_NS.objects.all()

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
                return render(request, 'silver.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': alldata,
                    'table_name':table_name
                }
                return render(request, 'silver.html', context)

        # Default behavior: show all data
        context = {'data': alldata,
                   'table_name':table_name
                   }
        return render(request, 'silver.html', context)




def faq(request):
    return render(request, 'faq.html')


def blank(request):
    return render(request, 'blank.html')


def error_404(request):
    return render(request, 'error_404.html')


def contact(request):
    return render(request, 'contact.html')

def stocksdd(request):
     
    category = 'Stocks'
    stocks1 = 'NIFTYBEES'
    stocks2 = 'ITBEES'
    stocks3 = 'SBIETFIT'
    context = {
        'nifty':stocks1,
        'it':stocks2,
        'sbi':stocks3,
        'category':category
    }
     
    return render(request,'stocksIndex.html',context)
 
def commoditiesdd(request):
    category = 'Commodities'
    com1 = 'SILVERBEES'
    com2 = 'GOLDBEES'
    
    context = {
        'silver':com1,
        'gold':com2,
        'category':category
        
    }
    return render(request,'commoditiesIndex.html',context)