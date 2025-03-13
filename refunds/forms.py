from django import forms
from django.core.cache import cache
from django.conf import settings
import requests
from django.core.exceptions import ValidationError

from .models import RefundRequest

class RefundRequestForm(forms.ModelForm):
    class Meta:
        model = RefundRequest
        exclude = ['user', 'status', 'iban_verified']  # fields auto-filled by the server
        widgets = {
            'order_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'products': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
        labels = {
            'order_number': 'Order Number',
            'order_date': 'Order Date',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'country': 'Country',
            'address': 'Address',
            'postal_code': 'Postal Code',
            'city': 'City',
            'products': 'Products to Refund',
            'reason': 'Reason for Refund',
            'bank_name': 'Bank Name',
            'account_type': 'Account Type',
            'iban': 'IBAN',
        }
        help_texts = {
            'iban': 'Enter IBAN for validation. It will be validated via an external API.',
        }

    def clean_iban(self):
        iban = self.cleaned_data.get('iban')
        if not iban:
            return iban

        cache_key = f'iban_validation_{iban}'
        cached_result = cache.get(cache_key)

        # Check if the IBAN validation result is already cached
        if cached_result is not None:
            if not cached_result:
                raise ValidationError('The IBAN entered is invalid.')
            self.cleaned_data['iban_verified'] = True
            return iban

        # Make an API request if validation result is not cached
        api_url = f'https://api.api-ninjas.com/v1/iban?iban={iban}'
        headers = {'X-Api-Key': settings.NINJAS_API_KEY}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            valid = data.get('valid', False)
            cache.set(cache_key, valid, 86400)  # Cache result for 24 hours
            if not valid:
                raise forms.ValidationError('The IBAN entered is invalid.')
            # Temporarily store IBAN validation result
            self.cleaned_data['iban_verified'] = valid
        else:
            raise forms.ValidationError('IBAN validation failed. Please try again later.')

        return iban

    def save(self, commit=True):
        refund_request = super().save(commit=False)
        iban = self.cleaned_data.get('iban')
        cache_key = f'iban_validation_{iban}'
        refund_request.iban_verified = cache.get(cache_key, False)  # Retrieve IBAN validation result from cache

        if commit:
            refund_request.save()
        return refund_request
