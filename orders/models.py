from django.db import models
# from django.conf import settings
from users.models import User
from services.models import Service
from uuid import uuid4
# Create your models here.

class ServiceOrder(models.Model):
    PENDING='Pending'
    IN_PROGRESS='In Progress'
    COMPLETED = 'Completed'
    CANCELED = 'Canceled'

    STATUS_CHOICES=[
        (PENDING,'Pending'),
        (IN_PROGRESS,'In Progress'),
        (COMPLETED,'Completed'),
        (CANCELED,'Canceled'),
    ]

    id=models.UUIDField(primary_key=True,default=uuid4,editable=False)
    buyer=models.ForeignKey(User,on_delete=models.CASCADE,related_name='order')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default=PENDING)
    total_price=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

class ServiceOrderItem(models.Model):
    order=models.ForeignKey(ServiceOrder,on_delete=models.CASCADE,related_name='items')
    service=models.ForeignKey(Service,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    total_price=models.DecimalField(max_digits=12,decimal_places=2)

    def __str__(self):
        return f'{self.quantity}x{self.service.title}'

class OrderNotification(models.Model):
    order=models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.order.id}"