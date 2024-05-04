from django.db import models

# Create your models here.from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    
    def calculate_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_orders = self.purchaseorder_set.all()

        if total_orders.exists() and completed_orders.exists():
            on_time_deliveries = completed_orders.filter(delivery_date__gte=F('delivered_date'))
            on_time_delivery_rate = on_time_deliveries.count() / completed_orders.count()
            self.on_time_delivery_rate = on_time_delivery_rate * 100
        else:
            self.on_time_delivery_rate = 0           

        quality_ratings = total_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
        if quality_ratings.exists():
            self.quality_rating_avg = sum(quality_ratings) / len(quality_ratings)

        response_times = total_orders.exclude(acknowledgment_date__isnull=True).annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date')).values_list('response_time', flat=True)
        if response_times.exists():
            response_times_in_seconds = [response.total_seconds() for response in response_times]
            self.average_response_time = sum(response_times_in_seconds) / len(response_times_in_seconds)

        self.fulfillment_rate = completed_orders.count() / total_orders.count() * 100

        self.save()

        

class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled')
    )

    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)  # Using string reference to avoid circular import
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Purchase Order #{self.id}"

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_performance_metrics(sender, instance, created, **kwargs):
    if instance.status == 'completed' or instance.quality_rating is not None or instance.acknowledgment_date is not None:
        print("Updating vendor performance metrics...")
        instance.vendor.calculate_performance_metrics()

