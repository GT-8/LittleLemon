"""from rest_framework.response import Response
from rest_framework.decorators import api_view"""

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm
from .models import *
from datetime import datetime
import json


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all().order_by('name')
    main_data = {"menu":menu_data}

    print(main_data)

    return render(request, 'menu.html', main_data)

def display_menu_items(request, pk=None):
    menu_item = ""

    if(pk):
        menu_item = Menu.objects.get(pk = pk)

    return render(request, 'menu_item.html', {"menu_item":menu_item})

