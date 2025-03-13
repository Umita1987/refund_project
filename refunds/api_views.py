from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .models import RefundRequest
from .serializers import RefundRequestSerializer, RefundRequestCreateSerializer


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or admins to access it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow access if user is an admin or the owner of the object
        return request.user.is_staff or obj.user == request.user


class RefundRequestViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for refund requests with JWT authentication.
    Admin can see all requests, while regular users only see their own.
    """
    serializer_class = RefundRequestSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]

    def get_serializer_class(self):
        # Choose serializer based on the action being performed
        if self.action in ['create', 'update', 'partial_update']:
            return RefundRequestCreateSerializer
        return RefundRequestSerializer

    def get_queryset(self):
        # Admins see all refund requests, regular users see only their own
        if self.request.user.is_staff:
            return RefundRequest.objects.all()
        return RefundRequest.objects.filter(user=self.request.user)
