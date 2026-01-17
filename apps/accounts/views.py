from rest_framework import viewsets
from apps.accounts.models import User
from apps.accounts.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Only admins manage users

