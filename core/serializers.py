from rest_framework import serializers
from .models import MercenaryProfile

class MercenaryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MercenaryProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_approved']
