from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import RefundRequestViewSet

router = DefaultRouter()
router.register(r'refunds', RefundRequestViewSet, basename='refundrequest')

urlpatterns = [
    path('', include(router.urls)),
]

