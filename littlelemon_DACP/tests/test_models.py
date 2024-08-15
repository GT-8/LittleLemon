from django.test import TestCase
from restaurant.models import Menu

class MenuTest(TestCase):
    def test_post_item(self):
        item  = Menu.objects.create(name="Test Cream", price=0.99, menu_item_description="Test Item")

        self.assertEqual(item.__str__(), "Test Cream : 0.99")
