from rest_framework import serializers
from .models import SupportTicket, CustomerInteraction
from accounts.serializers import UserSerializer
from services.serializers import ServiceRequestSerializer

class SupportTicketSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(read_only=True)
    service_request = ServiceRequestSerializer(read_only=True)
    service_request_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='service_request',
        queryset=ServiceRequestSerializer.Meta.model.objects.all()
    )

    class Meta:
        model = SupportTicket
        fields = (
            'id', 'service_request', 'service_request_id', 'assigned_to',
            'priority', 'status', 'description', 'resolution_notes',
            'created_at', 'updated_at', 'resolved_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'resolved_at')

class CustomerInteractionSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    support_rep = UserSerializer(read_only=True)
    support_ticket = SupportTicketSerializer(read_only=True)
    support_ticket_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='support_ticket',
        queryset=SupportTicket.objects.all()
    )

    class Meta:
        model = CustomerInteraction
        fields = (
            'id', 'support_ticket', 'support_ticket_id', 'customer',
            'support_rep', 'interaction_type', 'notes', 'created_at',
            'duration'
        )
        read_only_fields = ('id', 'created_at')

    def create(self, validated_data):
        validated_data['support_rep'] = self.context['request'].user
        return super().create(validated_data)

class SupportTicketDetailSerializer(SupportTicketSerializer):
    """
    Detailed serializer for support tickets including interactions
    """
    interactions = CustomerInteractionSerializer(many=True, read_only=True)

    class Meta(SupportTicketSerializer.Meta):
        fields = SupportTicketSerializer.Meta.fields + ('interactions',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        total_interaction_time = sum(
            interaction.duration or 0 
            for interaction in instance.interactions.all()
        )
        representation['total_interaction_time'] = total_interaction_time
        return representation
