from django.shortcuts import render,HttpResponseRedirect,redirect
from Custom_admin.models import *
from datetime import datetime,date
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            print(start_date, end_date)
            context = {
                'data': data,
                  'table_name':table_name
                
            }
            return render(request, 'nifty.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                  'table_name':table_name
            }
            return render(request, 'nifty.html', context)

    # Default behavior: show all data
    context = {
                'data': data,
               'table_name':table_name
               
               }
    return render(request, 'nifty.html', context)


def goldbees(request):
        table_name = 'GOLDBEES'

        alldata = GOLDBEES_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                     'table_name':table_name
                }
                return render(request, 'gold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                     'table_name':table_name
                }
                return render(request, 'gold.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   
                   'table_name':table_name
                   }
        return render(request, 'gold.html', context)



def itbees(request):
    table_name = 'ITBEES'
    alldata = ITBEES_NS.objects.all()
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
            print(start_date, end_date)
            context = {
                'data': data,
                  'table_name':table_name
            }
            return render(request, 'it.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                'table_name':table_name
            }
            return render(request, 'it.html', context)

    # Default behavior: show all data
    context = {
        'data': data,
        'table_name':table_name
               }
    return render(request, 'it.html', context)


def sbietfit(request):
    table_name = 'SBIETFIT'
    alldata = SBIETFIT_NS.objects.all()
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
            print(start_date, end_date)
            context = {
                'data': data,
                 'table_name':table_name
            }
            return render(request, 'sbi.html', context)
        else:
            # If start_date or end_date is not provided, show all data
            context = {
                'data': data,
                 'table_name':table_name
            }
            return render(request, 'sbi.html', context)

    # Default behavior: show all data
    context = {'data': data,
               'table_name':table_name
               }
    return render(request, 'sbi.html', context)


def silverbees(request):
        table_name = 'SILVERBEES'
        alldata = SILVERBEES_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'silver.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'silver.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'silver.html', context)



def egold(request):
        table_name = 'EGOLD'
        alldata = EGOLD_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'egold.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'egold.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'egold.html', context)



def abslnn50et(request):
        table_name = 'ABSLNN50ET'
        alldata = ABSLNN50ET_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'abslnn50et.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'abslnn50et.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'abslnn50et.html', context)

def commoietf(request):
        table_name = 'COMMOIETF'
        alldata = COMMOIETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'commoietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'commoietf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'commoietf.html', context)


def cpseetf(request):
        table_name = 'CPSEETF'
        alldata = COMMOIETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'cpseetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'cpseetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'cpseetf.html', context)


def dspitetf(request):
        table_name = 'DSPITETF'
        alldata = DSPITETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'dspitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'dspitetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'dspitetf.html', context)



def dspq50etf(request):
        table_name = 'DSPQ50ETF'
        alldata = DSPQ50ETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'dspq50.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'dspq50.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'dspq50.html', context)

def axistec(request):
        table_name = 'AXISTEC'
        alldata = AXISTECETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'axistec.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'axistec.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'axistec.html', context)


def icicib22(request):
        table_name = 'ICICIB22'
        alldata = ICICIB22_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'icicib22.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'icicib22.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'icicib22.html', context)


def infrabees(request):
        table_name = 'INFRABEES'
        alldata = INFRABEES_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'infrabees.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'infrabees.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'infrabees.html', context)


def iti(request):
        table_name = 'ITI'
        alldata = ITIETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'iti.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'iti.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'iti.html', context)


def kotak(request):
        table_name = 'KOTAK'
        alldata = KOTAKPSUBK_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'kotak.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'kotak.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'kotak.html', context)

def mafang(request):
        table_name = 'MAFANG'
        alldata = MAFANG_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'mafang.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'mafang.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'mafang.html', context)


def movalue(request):
        table_name = 'MOVALUE'
        alldata = MOVALUE_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'movalue.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'movalue.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'movalue.html', context)


def nifitetf(request):
        table_name = 'NIFITETF'
        alldata = NIFITETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'nifitetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'nifitetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'nifitetf.html', context)

def psubnk(request):
        table_name = 'PSUBNKIETF'
        alldata = PSUBNKIETF_NS.objects.all()
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'psubnkietf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'psubnkietf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'psubnkietf.html', context)




def tech(request):
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
                print(start_date, end_date)
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'techetf.html', context)
            else:
                # If start_date or end_date is not provided, show all data
                context = {
                    'data': data,
                    'table_name':table_name
                }
                return render(request, 'techetf.html', context)

        # Default behavior: show all data
        context = {'data': data,
                   'table_name':table_name
                   }
        return render(request, 'techetf.html', context)






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

    context = {
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
     
    return render(request,'stocksIndex.html',context)
 
def commoditiesdd(request):
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
    return render(request,'commoditiesIndex.html',context)