from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect
from django.contrib import messages
from .models import Exchange
from .forms import ExchangeForm

# Create your views here.


def exchange_index(request):
    exchanges = Exchange.objects.all()
    return render(request, 'exchange/index.html', {
        'exchanges': exchanges
    })


def exchange_detail(request, id):
    exchange = get_object_or_404(Exchange, id=id)
    return render(request, 'exchange/detail.html', {
        'exchange': exchange
    })


def exchange_create(request):
    # if request.method == 'POST':
    #     form = ExchangeForm(request.POST)
    #     if form.is_valid:
    #         form.save()
    # else:
    #     form = ExchangeForm()

    form = ExchangeForm(request.POST or None)
    if form.is_valid():
        savedExchange = form.save()
        messages.success(
            request, message="Operation is successfully processed!")
        return HttpResponseRedirect(savedExchange.get_detail_url())

    context = {
        'form': form
    }
    return render(request, 'exchange/form.html', context)


def exchange_update(request, id):
    exchange = get_object_or_404(Exchange, id=id)
    form = ExchangeForm(request.POST or None, instance=exchange)
    if form.is_valid():
        savedExchange = form.save()
        messages.success(
            request, message="Operation is successfully processed!")
        return HttpResponseRedirect(savedExchange.get_detail_url())

    context = {
        'form': form
    }
    return render(request, 'exchange/form.html', context)


def exchange_delete(request, id):
    exchange = get_object_or_404(Exchange, id=id)
    exchange.delete()
    return redirect(exchange.get_index_url())
