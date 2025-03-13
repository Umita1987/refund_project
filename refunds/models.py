from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RefundRequest(models.Model):
    """
    Model representing a refund request submitted by a user.
    """

    STATUS_CHOICES = [
        ('pending', 'Pending'),  # Request is under review
        ('approved', 'Approved'),  # Request has been approved
        ('rejected', 'Rejected'),  # Request has been rejected
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='refund_requests')
    order_number = models.CharField(max_length=100)  # Order reference number
    order_date = models.DateField()  # Date when the order was placed
    first_name = models.CharField(max_length=100)  # Customer's first name
    last_name = models.CharField(max_length=100)  # Customer's last name
    phone_number = models.CharField(max_length=20)  # Contact phone number
    email = models.EmailField()  # Customer's email address
    country = models.CharField(max_length=50)  # Country of residence
    address = models.TextField()  # Full address for the refund
    postal_code = models.CharField(max_length=20)  # Postal code
    city = models.CharField(max_length=50)  # City name
    products = models.TextField()  # List of products being returned
    reason = models.TextField()  # Reason for the refund request
    bank_name = models.CharField(max_length=200)  # Name of the bank
    account_type = models.CharField(max_length=50)  # Type of account (e.g., private, business)
    iban = models.CharField(max_length=34)  # International Bank Account Number
    iban_verified = models.BooleanField(default=False)  # Whether IBAN is verified via API
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Status of the refund request
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the request was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the request was last updated

    def __str__(self):
        return f"Refund #{self.id} - {self.order_number} ({self.status})"  # String representation of the model
