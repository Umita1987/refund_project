from django.urls import path
from .views import (
    CreateRefundRequestView,
    RefundRequestListView,
    RefundRequestDetailView,
    ValidateIBANView
)

urlpatterns = [
    path('refunds/', RefundRequestListView.as_view(), name='refund_list'),
    path('refunds/create/', CreateRefundRequestView.as_view(), name='create_refund'),
    path('refunds/<int:pk>/', RefundRequestDetailView.as_view(), name='refund_detail'),
    path('api/validate-iban/', ValidateIBANView.as_view(), name='validate_iban'),

]
