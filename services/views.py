from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import ServiceType, ServiceRequest, ServiceRequestComment
from .serializers import (
    ServiceTypeSerializer,
    ServiceRequestSerializer,
    ServiceRequestDetailSerializer,
    ServiceRequestCommentSerializer
)

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'priority', 'service_type']
    search_fields = ['description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(customer=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ServiceRequestDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        service_request = self.get_object()
        status = request.data.get('status')
        
        if status not in dict(ServiceRequest.STATUS_CHOICES):
            return Response(
                {'detail': 'Invalid status'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if status == 'COMPLETED':
            service_request.completed_at = timezone.now()
        
        service_request.status = status
        service_request.save()
        
        serializer = self.get_serializer(service_request)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        service_request = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            return Response(
                {'detail': 'assigned_to is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            service_request.assigned_to_id = assigned_to_id
            service_request.save()
            serializer = self.get_serializer(service_request)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ServiceRequestCommentViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequestComment.objects.all()
    serializer_class = ServiceRequestCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        service_request_id = self.kwargs.get('service_request_pk')
        if service_request_id:
            return self.queryset.filter(service_request_id=service_request_id)
        return self.queryset.none()

    def perform_create(self, serializer):
        service_request_id = self.kwargs.get('service_request_pk')
        serializer.save(
            user=self.request.user,
            service_request_id=service_request_id
        )
