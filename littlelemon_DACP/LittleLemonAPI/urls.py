from django.urls import path
from .views import *

urlpatterns = [

        path('menu-items', GetMenu.as_view()),
        path('menu-items/<int:pk>', GetMenuItem.as_view()),
        path('orders', GetOrders.as_view()),
        path('orders/<int:pk>', GetOrder.as_view()),
        path('cart/menu-items', CartContent.as_view()),
        path('groups/manager/users', ManagerUsersView.as_view()),
        path('groups/manager/users/<int:pk>', ManagerUserView.as_view()),
        path('groups/delivery-crew/users', DeliveryCrewManagement.as_view()),
        path('groups/delivery-crew/users/<int:pk>', DeliveryManagement.as_view()),
]

