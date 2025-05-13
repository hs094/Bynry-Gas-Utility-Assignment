from rest_framework import serializers
from .models import ServiceType, ServiceRequest, ServiceRequestComment
from accounts.serializers import UserSerializer

class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ('id', 'name', 'description', 'estimated_time', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class ServiceRequestCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ServiceRequestComment
        fields = ('id', 'service_request', 'user', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    service_type = ServiceTypeSerializer(read_only=True)
    service_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ServiceType.objects.all(),
        write_only=True,
        source='service_type'
    )
    comments = ServiceRequestCommentSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceRequest
        fields = (
            'id', 'customer', 'service_type', 'service_type_id', 'description',
            'status', 'priority', 'attachment', 'created_at', 'updated_at',
            'completed_at', 'assigned_to', 'comments'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'completed_at')

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user
        return super().create(validated_data)

class ServiceRequestDetailSerializer(ServiceRequestSerializer):
    """
    Detailed serializer for service requests with additional information
    """
    class Meta(ServiceRequestSerializer.Meta):
        fields = ServiceRequestSerializer.Meta.fields + ('support_tickets',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['support_tickets'] = [
            {
                'id': ticket.id,
                'status': ticket.status,
                'priority': ticket.priority,
                'created_at': ticket.created_at,
                'resolved_at': ticket.resolved_at
            }
            for ticket in instance.support_tickets.all()
        ]
        return representation
