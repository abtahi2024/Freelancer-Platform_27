from orders.models import ServiceOrder, ServiceOrderItem
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from services.models import Service
from django.shortcuts import get_object_or_404
class ServiceOrderService:
    @staticmethod
    def create_order(buyer, services_data):
        """
        buyer: User instance
        services_data: list of dicts [{service: id, quantity: n}, ...]
        """
        if not services_data:
            raise ValidationError({'detail': "No services provided"})

        with transaction.atomic():
            order = ServiceOrder.objects.create(buyer=buyer, total_price=0)
            total_price = 0

            for item in services_data:
                service_id = item.get('service_id')
                quantity = item.get('quantity', 1)

                try:
                    service = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    raise ValidationError({'service_id': f"Service with id {service_id} does not exist"})

                price = service.price
                total = price * quantity

                ServiceOrderItem.objects.create(
                    order=order,
                    service=service,
                    quantity=quantity,
                    price=price,
                    total_price=total
                )
                total_price += total

            order.total_price = total_price
            order.save()
            return order

    
    @staticmethod
    def cancel_order(order, user):
        """
        Cancel a service order if allowed.
        Staff can cancel any order.
        Buyer can cancel only their own order if not completed.
        """
        if user.is_staff:
            order.status = ServiceOrder.CANCELED
            order.save()
            return order

        if order.buyer != user:
            raise PermissionDenied({"detail": "You can only cancel your own order"})

        if order.status == ServiceOrder.COMPLETED:
            raise ValidationError({"detail": "You cannot cancel a completed order"})

        order.status = ServiceOrder.CANCELED
        order.save()
        return order