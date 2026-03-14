from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Vendor

class VendorTests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name='Test Vendor', code='TEST001', description='Test description')
        self.url = reverse('vendor-list-create')
        self.detail_url = reverse('vendor-detail', kwargs={'pk': self.vendor.pk})

    def test_list_vendors(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.vendor.name)

    def test_create_vendor(self):
        data = {'name': 'New Vendor', 'code': 'NEW001', 'description': 'New description'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 2)

    def test_get_vendor_detail(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.vendor.name)

    def test_update_vendor(self):
        data = {'name': 'Updated Vendor', 'code': 'UPD001', 'description': 'Updated description'}
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Vendor.objects.get(pk=self.vendor.pk).name, 'Updated Vendor')

    def test_delete_vendor(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 0)
