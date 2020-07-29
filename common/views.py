from django.shortcuts import render, HttpResponse

# Create your views here.


def home_view(request):
    context = {
        'message': 'This is a message sent from view to template'
    }
    return render(request, 'home.html', context)
