from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import SupportTicket, CustomerInteraction
from .serializers import (
    SupportTicketSerializer,
    SupportTicketDetailSerializer,
    CustomerInteractionSerializer
)

class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status', 'priority']
    search_fields = ['description']

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(service_request__customer=user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SupportTicketDetailSerializer
        return self.serializer_class

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        ticket = self.get_object()
        resolution_notes = request.data.get('resolution_notes')
        
        if not resolution_notes:
            return Response(
                {'detail': 'Resolution notes are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ticket.status = 'RESOLVED'
        ticket.resolution_notes = resolution_notes
        ticket.resolved_at = timezone.now()
        ticket.save()
        
        serializer = self.get_serializer(ticket)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        ticket = self.get_object()
        assigned_to_id = request.data.get('assigned_to')
        
        if not assigned_to_id:
            return Response(
                {'detail': 'assigned_to is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            ticket.assigned_to_id = assigned_to_id
            ticket.save()
            serializer = self.get_serializer(ticket)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CustomerInteractionViewSet(viewsets.ModelViewSet):
    queryset = CustomerInteraction.objects.all()
    serializer_class = CustomerInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(customer=user)

    @action(detail=False, methods=['get'])
    def recent_interactions(self, request):
        user = request.user
        recent = self.get_queryset().order_by('-created_at')[:5]
        serializer = self.get_serializer(recent, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def interaction_stats(self, request):
        user = request.user
        interactions = self.get_queryset()
        
        total_duration = sum(
            interaction.duration or 0 
            for interaction in interactions
        )
        
        by_type = {}
        for interaction in interactions:
            type_name = interaction.get_interaction_type_display()
            by_type[type_name] = by_type.get(type_name, 0) + 1
            
        return Response({
            'total_interactions': interactions.count(),
            'total_duration_minutes': total_duration,
            'interactions_by_type': by_type
        })
