from rest_framework.serializers import ModelSerializer
from .models import Booking

class BookingSerializer(ModelSerializer):
    model = Booking
    fields = "__all__"
