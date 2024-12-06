from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Item, UserPhoneNumber, NotificationPreference

class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        user = User.objects.create_user(**validated_data)
        UserPhoneNumber.objects.create(user=user, phone_number=phone_number)
        return user
    
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "owner", "name", "category", "purchase_date", "price", "warranty_expiration", "image"]
        extra_kwargs = {"owner": {"read_only": True}}

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ['id', 'user', 'item', 'notify_when']
        read_only_fields = ['id']