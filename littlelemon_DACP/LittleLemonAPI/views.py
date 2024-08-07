from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from .serializers import MenuSerializer, UserSerializer, CartSerializer, OrderSerializer
from .models import Menu, OrderItem, Order, Cart
from .permissions import *
from decimal import Decimal


class GetMenu(generics.ListAPIView, generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    ordering_fields = ['price', 'dish']
    search_fields = ['name']

    def get_permissions(self):
        if(self.request.method == 'POST'):
            return [ManagerPermission(), IsAdminUser()]

        return [AllowAny()]


class GetMenuItem(generics.RetrieveUpdateDestroyAPIView, generics.RetrieveAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_permissions(self):
        if(self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE' or self.request.method == 'PATCH'):
            return [ManagerPermission(), IsAdminUser()]

        return [AllowAny()]


class GetOrders(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def perform_create(self, serializer):
        print(self.request.user)

        cart_items = Cart.objects.filter(user=self.request.user)
        total = self.calculate_total(cart_items)
        order = serializer.save(user=self.request.user, total=total)

        for cart_item in cart_items:
            OrderItem.objects.create(item=cart_item.item, quantity=cart_item.quantity,
                                     unit_price=cart_item.unit_price, price=cart_item.total_price, order=order)
            cart_item.delete()

    def get_queryset(self):
        user = self.request.user

        if(user.groups.filter(name='Manager').exists()):
            return Order.objects.all()
        elif(user.groups.filter(name='Delivery crew').exists()):
            return Order.objects.filter(delivery_crew=user)

        return Order.objects.filter(user=user)

    def get_permissions(self):
        if(self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'PATCH'):
            return [CustomerPermission()]

        return [AllowAny()]

    def calculate_total(self, cart_items):
        total = Decimal(0)

        for item in cart_items:
            total += item.total_price
        return total


class GetOrder(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if(user.groups.filter(name='Manager').exists()):
            return Order.objects.all()
        elif(user.groups.filter(name='Delivery crew').exists()):
            return Order.objects.filter(delivery_crew=user)

        return Order.objects.filter(user=user)

    """def get_permissions(self):
        if(self.request.method == 'PUT'):
            return [ManagerPermission()]
        elif(self.request.method == 'PATCH'):
            return [DeliveryPermission(), ManagerPermission()]

        return [AllowAny()]"""


class CartContent(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [CustomerPermission]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        item = self.request.data.get('item')
        quantity = int(self.request.data.get('quantity'))
        unit_price = Menu.objects.get(pk=item).price
        cost = quantity * unit_price

        serializer.save(user=self.request.user, total_price=cost)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()

        return Response(status=204)

class ManagerUsersView(APIView):

    def get(self, request):
        return Response(UserSerializer(User.objects.filter(groups=Group.objects.get(name='Manager')), many=True).data)

    def post(self, request):
        name = request.POST.get('username')

        if(name):
            
            user = get_object_or_404(User, username=name)

            if(user):
                user.groups.add(Group.objects.get(name='Manager'))
                return Response(request.data, status=status.HTTP_201_CREATED)

            return Response({"No such user " + name})
            
        return Response({"N":"A"})

    def get_permissions(self):
        if(self.request.method == 'GET'):
            return [ManagerPermission()]

        return [IsAdminUser()]


class ManagerUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if(user):
            user.groups.remove(Group.objects.get(name='Manager'))
            return Response(request.data)

        return Response({"No such user " + name})


class DeliveryCrewManagement(APIView):
    permission_classes = [ManagerPermission]

    def get(self, request):
        return Response(UserSerializer(User.objects.filter(groups=Group.objects.get(name='Delivery crew')), many=True).data)

    def post(self, request):
        name = request.POST.get('username')

        if(name):
            
            user = get_object_or_404(User, username=name)

            if(user):
                user.groups.add(Group.objects.get(name='Delivery crew'))
                return Response(request.data, status=status.HTTP_201_CREATED)

            return Response({"No such user " + name})
            
        return Response({"N":"A"})


class DeliveryManagement(APIView):
    permission_classes = [ManagerPermission]

    def delete(self, request, pk):
        user = get_object_or_404(User, id=pk)

        if(user):
            user.groups.remove(Group.objects.get(name='Delivery crew'))
            return Response(request.data)

        return Response({"No such user " + name})
