from rest_framework import status
from rest_framework.test import APITestCase
from orders.models import Order


class OrderTests(APITestCase):
    def setUp(self):
        self.order = Order.objects.create(
            table_number=1, items=[{"name": "Burger", "price": 8.99}], status="pending"
        )

    def test_create_order(self):
        data = {
            "table_number": 2,
            "items": [{"name": "Burger", "price": 8.99}],
            "status": "pending",
        }
        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_update_order(self):
        data = {
            "table_number": 1,
            "items": [{"name": "Pizza", "price": 12.99}],
            "status": "ready",
        }
        response = self.client.put(f"/api/orders/{self.order.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.items[0]["price"], 12.99)
        self.assertEqual(self.order.status, "ready")

    def test_delete_order(self):
        response = self.client.delete(f"/api/orders/{self.order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
