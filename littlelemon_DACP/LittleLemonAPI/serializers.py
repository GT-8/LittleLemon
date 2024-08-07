from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['name', 'price', 'menu_item_description', 'dish']


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'order_items']
        extra_kwargs = {
            'total': {'read_only': True},
            'user': {'read_only': True}
        }

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True, context={'request': self.context['request']})
        return serializer.data


class OrderItemSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='item.price', read_only=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
    name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'item': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='item.price', read_only=True)
    name = serializers.CharField(source='item.name', read_only=True)

    class Meta:
        model = Cart
        fields = ['user_id', 'item', 'name', 'quantity', 'unit_price', 'total_price']
        extra_kwargs = {
            'total_price': {'read_only': True}
        }

