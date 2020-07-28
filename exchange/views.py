from django.shortcuts import render, HttpResponse

# Create your views here.


def exchange_home_view(request):
    return HttpResponse('exchange home veiw')


def exchange_create_view(request):
    return HttpResponse('exchange create veiw')


def exchange_update_view(request):
    return HttpResponse('exchange update veiw')


def exchange_delete_view(request):
    return HttpResponse('exchange delete veiw')


def exchange_detail_view(request):
    return HttpResponse('exchange detail veiw')
