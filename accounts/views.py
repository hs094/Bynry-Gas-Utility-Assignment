from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from .models import CustomerProfile, SupportRepresentative
from .serializers import (
    UserSerializer,
    CustomerProfileSerializer,
    SupportRepresentativeSerializer
)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                         context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_staff': user.is_staff
        })

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        try:
            profile = self.queryset.get(user=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except CustomerProfile.DoesNotExist:
            return Response(
                {'detail': 'Profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def get_token(self, request):
        """
        Get or create an authentication token for the current user.
        """
        token, created = Token.objects.get_or_create(user=request.user)
        return Response({
            'token': token.key,
            'created': created
        })

class SupportRepresentativeViewSet(viewsets.ModelViewSet):
    queryset = SupportRepresentative.objects.all()
    serializer_class = SupportRepresentativeSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'])
    def available_representatives(self, request):
        available_reps = self.queryset.filter(user__is_active=True)
        serializer = self.get_serializer(available_reps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def current_workload(self, request, pk=None):
        rep = self.get_object()
        assigned_tickets = rep.user.assigned_tickets.filter(
            status__in=['OPEN', 'IN_PROGRESS']
        ).count()
        return Response({
            'representative': self.get_serializer(rep).data,
            'active_tickets': assigned_tickets
        })
