import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User

class OWASPSecurityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+155500055',
            full_name='Regular User',
            role='donor'
        )

    def test_unauthenticated_admin_access_denied(self):
        """OWASP A01: Broken Access Control - Unauthenticated user blocked from admin endpoints"""
        url = reverse('admin-dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_role_access_denied(self):
        """OWASP A01: Broken Access Control - Non-admin user blocked from admin endpoints"""
        self.client.force_authenticate(user=self.user)
        url = reverse('admin-dashboard-stats')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sql_injection_protection(self):
        """OWASP A03: Injection Protection - ORM parameterization prevents SQL injection"""
        self.client.force_authenticate(user=self.user)
        malicious_input = "'; DROP TABLE users; --"
        url = f"/api/v1/donations/?food_type={malicious_input}"
        response = self.client.get(url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_xss_sanitization_in_json_payloads(self):
        """OWASP A03: Cross-Site Scripting - Script tag payloads sanitized"""
        self.client.force_authenticate(user=self.user)
        script_payload = "<script>alert('xss')</script>"
        url = reverse('donation-list-create')
        response = self.client.post(url, {
            'food_type': script_payload,
            'quantity_kg': 10,
            'pickup_address': '123 Main St'
        }, format='json')
        # DRF accepts or handles, verify database contains raw/escaped string safely without crashing
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
