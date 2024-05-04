from rest_framework import viewsets
from rest_framework import status
from django.utils import timezone
from rest_framework.response import Response 
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Handle partial argument
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response(status=status.HTTP_200_OK)

    # def update(self, request, pk=None):
    #     purchase_order = self.get_object()
    #     serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         if 'acknowledgment_date' in serializer.validated_data:
    #             purchase_order.vendor.calculate_performance_metrics()
    #         return Response(serializer.data)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VendorPerformanceViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor)
        return Response({
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        })



