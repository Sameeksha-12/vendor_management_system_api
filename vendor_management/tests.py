from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some test vendors
        self.vendor1 = Vendor.objects.create(
            name='Vendor 1', 
            contact_details='Vendor 1 contact details', 
            address='Vendor 1 address', 
            vendor_code='V1',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=10.5,
            fulfillment_rate=90.0
        )
        self.vendor2 = Vendor.objects.create(
            name='Vendor 2', 
            contact_details='Vendor 2 contact details', 
            address='Vendor 2 address', 
            vendor_code='V2',
            on_time_delivery_rate=85.0,
            quality_rating_avg=4.0,
            average_response_time=15.5,
            fulfillment_rate=80.0
        )

    def test_list_vendors(self):
        response = self.client.get('/api/vendors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if all vendors are returned

    def test_retrieve_vendor(self):
        response = self.client.get(reverse('vendor-detail', kwargs={'pk': self.vendor1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Vendor 1')  # Check if correct vendor is retrieved


class PurchaseOrderAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create some test vendors
        self.vendor1 = Vendor.objects.create(
            name='Vendor 1', 
            contact_details='Vendor 1 contact details', 
            address='Vendor 1 address', 
            vendor_code='V1'
        )
        self.vendor2 = Vendor.objects.create(
            name='Vendor 2', 
            contact_details='Vendor 2 contact details', 
            address='Vendor 2 address', 
            vendor_code='V2'
        )

        # Create some test purchase orders
        self.po1 = PurchaseOrder.objects.create(
            vendor=self.vendor1, 
            order_date='2024-05-04T08:00:00Z',
            delivery_date='2024-05-10T08:00:00Z',
            items=[{
                "name": "Item 1",
                "price": 10,
                "quantity": 2
            },
            {
                "name": "Item 2",
                "price": 50,
                "quantity": 1
            }],
            quantity=10,
            status='completed',
            quality_rating=4.5,
            issue_date='2024-05-03T08:00:00Z',
            acknowledgment_date='2024-05-03T09:00:00Z'
        )
        self.po2 = PurchaseOrder.objects.create(
            vendor=self.vendor2, 
            order_date='2024-05-05T08:00:00Z',
            delivery_date='2024-05-12T08:00:00Z',
            items=[{
                "name": "Item 1",
                "price": 10,
                "quantity": 2
            },
            {
                "name": "Item 2",
                "price": 50,
                "quantity": 1
            }],
            quantity=15,
            status='pending',
            issue_date='2024-05-04T08:00:00Z'
        )

    def test_list_purchase_orders(self):
        response = self.client.get('/api/purchase_orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Check if all purchase orders are returned

    def test_retrieve_purchase_order(self):
        response = self.client.get(reverse('purchaseorder-detail', kwargs={'pk': self.po1.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['vendor'], self.vendor1.id)  # Check if correct purchase order is retrieved

    
