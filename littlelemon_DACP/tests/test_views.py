from django.test import TestCase, Client
from rest_framework.test import APIClient
from restaurant.models import Menu
from LittleLemonAPI.serializers import MenuSerializer

class MenuTest(TestCase):

    def setUp(self):
        Menu.objects.create(name="TestCream", price=1.8, menu_item_description="test 1", dish="Main Test")
        Menu.objects.create(name="Testlate", price=2.4, menu_item_description="test 2", dish="Testlad")

    def test_getall(self):
        client = APIClient()

        for i in Menu.objects.all():
            response = client.get("http://127.0.0.1:8000/api/menu-items/" + str(i.id))
            self.assertEqual(response.data, MenuSerializer(i).data)
                

class MenuItemTest(TestCase):

    def setUp(self):
        self.item = Menu.objects.create(name="TestBerry", price=0.8, menu_item_description="test i")

    def test_getitem(self):
        client = APIClient()

        serialized = MenuSerializer(self.item)
        response = client.get("http://127.0.0.1:8000/api/menu-items/" + str(self.item.id))

        self.assertEqual(response.data, serialized.data)
