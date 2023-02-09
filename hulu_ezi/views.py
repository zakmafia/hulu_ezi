from django.shortcuts import render
from datetime import datetime
current_year = datetime.now().year

def index(request):
    context = {
        'current_year': current_year
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'current_year': current_year
    }
    return render(request, 'about.html', context)