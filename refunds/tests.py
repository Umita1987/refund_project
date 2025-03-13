from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from unittest.mock import patch

from .models import RefundRequest
from .forms import RefundRequestForm

User = get_user_model()


class RefundRequestFormTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')

    @patch('refunds.forms.requests.get')
    def test_clean_iban_valid(self, mock_get):
        """Check that the form accepts a valid IBAN."""
        # Simulate a correct response from an external API
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'valid': True}

        data = {
            'order_number': '100',
            'order_date': '2025-03-12',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '123456789',
            'email': 'test@example.com',
            'country': 'DE',
            'address': 'Test Address',
            'postal_code': '12345',
            'city': 'Berlin',
            'products': 'Product 1, Product 2',
            'reason': 'Test Reason',
            'bank_name': 'Test Bank',
            'account_type': 'private',
            'iban': 'DE89370400440532013000'
        }
        form = RefundRequestForm(data=data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    @patch('refunds.forms.requests.get')
    def test_clean_iban_invalid(self, mock_get):
        """Check that the form rejects an invalid IBAN."""
        # Simulate an external API response with a validity of False
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'valid': False}

        data = {
            'order_number': '101',
            'order_date': '2025-03-12',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '123456789',
            'email': 'test@example.com',
            'country': 'DE',
            'address': 'Test Address',
            'postal_code': '12345',
            'city': 'Berlin',
            'products': 'Product 1, Product 2',
            'reason': 'Test Reason',
            'bank_name': 'Test Bank',
            'account_type': 'private',
            'iban': 'DE89370400440532013001'  # Invalid IBAN
        }
        form = RefundRequestForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('iban', form.errors)


class RefundRequestAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='apiuser', password='apipass', email='api@example.com')
        self.client.login(username='apiuser', password='apipass')
        self.refund_request = RefundRequest.objects.create(
            user=self.user,
            order_number='102',
            order_date='2025-03-12',
            first_name='API',
            last_name='User',
            phone_number='987654321',
            email='api@example.com',
            country='DE',
            address='API Address',
            postal_code='54321',
            city='Munich',
            products='Product A, Product B',
            reason='Testing API',
            bank_name='API Bank',
            account_type='private',
            iban='DE89370400440532013000'
        )

    def test_api_list(self):
        """Check that the API returns a list of requests for the current user."""
        url = reverse('refundrequest-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.refund_request.order_number)

    def test_api_detail(self):
        """Checking receipt of request details by ID via API."""
        url = reverse('refundrequest-detail', kwargs={'pk': self.refund_request.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.refund_request.first_name)


class RefundRequestSignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='signaluser', password='signalpass', email='signal@example.com')
        self.refund_request = RefundRequest.objects.create(
            user=self.user,
            order_number='103',
            order_date='2025-03-12',
            first_name='Signal',
            last_name='User',
            phone_number='111222333',
            email='signal@example.com',
            country='DE',
            address='Signal Address',
            postal_code='11111',
            city='Hamburg',
            products='Product X',
            reason='Signal Test',
            bank_name='Signal Bank',
            account_type='private',
            iban='DE89370400440532013000',
            status='pending'
        )
        # Clear the test backend mailbox
        mail.outbox = []

    def test_status_change_email_sent(self):
        """We check that an email is sent when the status changes."""
        self.refund_request.status = 'approved'
        self.refund_request.save()
        self.assertEqual(len(mail.outbox), 1)
        # Check that the subject of the letter contains keywords
        self.assertIn('Статус вашего запроса', mail.outbox[0].subject)
        self.assertIn('изменён', mail.outbox[0].subject)


class RefundRequestNegativeAPITest(TestCase):
    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='pass1', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='pass2', email='user2@example.com')

        # Create a request for user user1
        self.refund1 = RefundRequest.objects.create(
            user=self.user1,
            order_number='200',
            order_date='2025-04-01',
            first_name='User1',
            last_name='Test',
            phone_number='111111',
            email='user1@example.com',
            country='DE',
            address='Address1',
            postal_code='10001',
            city='Berlin',
            products='Product 1',
            reason='Test reason',
            bank_name='Bank1',
            account_type='private',
            iban='DE89370400440532013000'
        )
        # Clients for user1 and user2 (use session authentication if enabled)
        self.client1 = Client()
        self.client2 = Client()
        self.client1.login(username='user1', password='pass1')
        self.client2.login(username='user2', password='pass2')

    def test_unauthorized_access(self):
        """Check that a request without authentication returns 401."""
        client = Client()  # без авторизации
        url = reverse('refundrequest-list')
        response = client.get(url)
        self.assertEqual(response.status_code, 401)

    def test_access_object_not_owned(self):
        """User2 should not have access to a request owned by user1."""
        url = reverse('refundrequest-detail', kwargs={'pk': self.refund1.pk})
        response = self.client2.get(url)
        # Our permission (IsOwnerOrAdmin) can return 403 or 404 – we check that access is denied.
        self.assertIn(response.status_code, [403, 404])

    def test_update_object_not_owned(self):
        """User2 cannot update a query owned by user1."""
        url = reverse('refundrequest-detail', kwargs={'pk': self.refund1.pk})
        data = {'status': 'approved'}
        response = self.client2.patch(url, data, content_type='application/json')
        self.assertIn(response.status_code, [403, 404])

    def test_delete_object_not_owned(self):
        """User2 cannot delete a request belonging to user1."""
        url = reverse('refundrequest-detail', kwargs={'pk': self.refund1.pk})
        response = self.client2.delete(url)
        self.assertIn(response.status_code, [403, 404])