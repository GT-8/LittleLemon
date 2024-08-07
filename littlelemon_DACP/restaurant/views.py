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

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

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

#@api_view(['GET'])
@csrf_exempt
def bookings(request):
    if(request.method == 'POST'):
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(reservation_slot=data['reservation_slot']).exists()

        if(not exist):
            booking = Booking(first_name=data['first_name'],
                              reservation_date=data['reservation_date'],
                              reservation_slot=data['reservation_slot'],
                              guest_number=1)
            booking.save()

        return HttpResponse({"error":1}, content_type='application/json')

    date = request.GET.get('date', datetime.today().date())

    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)#{"bookings":bookings}

    #return Response({"bookings":booking_json})
    return HttpResponse(booking_json, content_type='application/json')#render(request, 'bookings.html', {"bookings":booking_json})#booking_json)
