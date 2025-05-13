from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomerProfile, SupportRepresentative

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerProfile
        fields = ('id', 'user', 'customer_id', 'phone_number', 'address', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        customer_profile = CustomerProfile.objects.create(user=user, **validated_data)
        return customer_profile

class SupportRepresentativeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SupportRepresentative
        fields = ('id', 'user', 'employee_id', 'department', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        support_rep = SupportRepresentative.objects.create(user=user, **validated_data)
        return support_rep
