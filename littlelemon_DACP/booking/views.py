from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core import serializers
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import BookingForm
from .models import Booking
from .serializers import BookingSerializer
from datetime import datetime
import json

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

@csrf_exempt
def bookings(request):
    if(request.method == 'POST'):
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(reservation_slot=data['reservation_slot']).exists()

        if(not exist):
            booking = Booking(first_name=data['first_name'],
                              reservation_date=data['reservation_date'],
                              reservation_slot=data['reservation_slot'],)

            booking.save()

        return HttpResponse({"error":1}, content_type='application/json')

    date = request.GET.get('date', datetime.today().date())

    bookings = Booking.objects.filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    if(request.GET.get('api')):
        return HttpResponse(booking_json, content_type='application/json')

    return render(request, 'bookings.html', {"bookings":booking_json})

class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()

    serializer_class = BookingSerializer
    premission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
