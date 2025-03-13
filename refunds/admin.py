from django.contrib import admin
from .models import RefundRequest
from import_export.admin import ImportExportModelAdmin

@admin.register(RefundRequest)
class RefundRequestAdmin(ImportExportModelAdmin):
    list_display = ('id', 'order_number', 'user', 'status', 'created_at', 'country')
    list_filter = ('status', 'created_at', 'country')
    search_fields = ('order_number', 'user__username', 'email')

    # Fields displayed in the edit form
    fields = (
        'user',
        'order_number',
        'order_date',
        'first_name',
        'last_name',
        'phone_number',
        'email',
        'country',
        'address',
        'postal_code',
        'city',
        'products',
        'reason',
        'bank_name',
        'account_type',
        'iban',
        'iban_verified',
        'status',  # <-- Important: ensure the status field is included here
    )
