from rest_framework import serializers
from .models import Customer, IPAddress

class CustomerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Customer
    fields = '__all__'

class IPAddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = IPAddress
    fields = '__all__'

class AllocateIPSerializer(serializers.Serializer):
  customer_name = serializers.CharField(max_length=255)
  email = serializers.EmailField()
