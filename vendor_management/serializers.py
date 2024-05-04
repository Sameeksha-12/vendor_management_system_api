from rest_framework import serializers
from .models import Vendor, PurchaseOrder

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['acknowledgment_date'] = instance.acknowledgment_date
        return data
