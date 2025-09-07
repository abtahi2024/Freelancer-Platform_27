from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from orders.models import ServiceOrder
from orders.serializers import ServiceOrderSerializer,CreateServiceOrderSerializer,UpdateServiceOrderSerializer
from orders.services import ServiceOrderService 
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ServiceOrderViewSet(ModelViewSet):
    """
    ViewSet for Service Orders
    - create order with multiple services
    - update order status (staff only)
    - cancel order
    - list / retrieve orders
    """

    http_method_names=['get','post','patch','delete','head','options']

    def get_permissions(self):
        if self.action in ['update','partial_update','destroy','update_status']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action=='create':
            return CreateServiceOrderSerializer
        elif self.action in ['update','partial_update']:
            return UpdateServiceOrderSerializer
        return ServiceOrderSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            context['buyer']=None
        else:
            if self.request.user.is_authenticated:
                context['buyer'] = self.request.user 
            else: None
        return context

    def get_queryset(self):
        """
        Staff: see all orders
        Buyer: see only own orders
        """
        if getattr(self,'swagger_fake_view',False):
            return ServiceOrder.objects.none()
        

        if self.request.user.is_staff:
            return ServiceOrder.objects.prefetch_related('items__service').all()
        elif self.request.is_authenticated:
            return ServiceOrder.objects.prefetch_related('items__service').filter(buyer=self.request.user)
        return ServiceOrder.objects.none()
    
    @swagger_auto_schema(
        operation_summary="List all service orders",
        operation_description="Admins see all orders. Buyers only see their own orders.",
        responses={200: ServiceOrderSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve order details",
        responses={200: ServiceOrderSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a new service order",
        operation_description="Create an order with multiple services (Authenticated users only)",
        request_body=CreateServiceOrderSerializer,
        responses={201: ServiceOrderSerializer, 400: "Bad request"},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update service order (Admin only)",
        operation_description="Admins can update order fields like status, price, etc.",
        request_body=UpdateServiceOrderSerializer,
        responses={200: ServiceOrderSerializer, 400: "Bad request"},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update service order (Admin only)",
        request_body=UpdateServiceOrderSerializer,
        responses={200: ServiceOrderSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete a service order (Admin only)",
        responses={204: "Order deleted successfully"},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        method="post",
        operation_summary="Cancel a service order",
        operation_description="Buyers can cancel their own orders. Admins can cancel any order.",
        responses={200: ServiceOrderSerializer, 400: "Bad request"},
    )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a service order
        """
        order = self.get_object()
        try:
            updated_order = ServiceOrderService.cancel_order(order, request.user)
            return Response(ServiceOrderSerializer(updated_order).data)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
        
    @swagger_auto_schema(
        method="patch",
        operation_summary="Update order status (Admin only)",
        operation_description="Admins can update order status (Pending, In Progress, Completed, Canceled).",
        request_body=UpdateServiceOrderSerializer,
        responses={200: "Order status updated", 400: "Bad request"},
    )
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Staff can update order status
        """
        order = self.get_object()
        serializer = UpdateServiceOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f"Order status updated to {request.data.get('status')}"})
