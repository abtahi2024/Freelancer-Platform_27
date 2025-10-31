from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,api_view
from rest_framework.permissions import IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from orders.models import ServiceOrder,ServiceOrderItem
from orders.serializers import ServiceOrderSerializer,CreateServiceOrderSerializer,UpdateServiceOrderSerializer
from orders.services import ServiceOrderService 
from drf_yasg.utils import swagger_auto_schema
from sslcommerz_lib import SSLCOMMERZ 
from rest_framework import status
from django.conf import settings as main_setting
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
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
        return [IsAuthenticatedOrReadOnly()]
        # return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action=='create':
            return CreateServiceOrderSerializer
        elif self.action in ['update','partial_update']:
            return UpdateServiceOrderSerializer
        return ServiceOrderSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['buyer'] = self.request.user if self.request.user.is_authenticated else None
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
        elif self.request.user.is_authenticated:
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


# @api_view(['POST'])
# def initiate_payment(request):
#     user=request.user
#     amount=request.data.get("amount")
#     order_id=request.data.get("orderId")
#     num_items=request.data.get("numItems")

#     settings = { 'store_id':'phima68e538afdcefc', 'store_pass': 'phima68e538afdcefc@ssl', 'issandbox': True }
#     sslcz = SSLCOMMERZ(settings)
#     post_body = {}
#     post_body['total_amount'] = amount
#     post_body['currency'] = "BDT"
#     post_body['tran_id'] = f"trx_{order_id}"
#     post_body['success_url'] = f"{main_setting.BACKEND_URL}/api/v1/payment/success/"
#     post_body['fail_url'] = f"{main_setting.BACKEND_URL}/api/v1/payment/fail/"
#     post_body['cancel_url'] = f"{main_setting.BACKEND_URL}/api/v1/payment/cancel/"
#     post_body['emi_option'] = 0
#     post_body['cus_name'] = f"{user.first_name} {user.last_name}"
#     post_body['cus_email'] = user.email
#     post_body['cus_phone'] = user.phone_number
#     post_body['cus_add1'] = user.address
#     post_body['cus_city'] = "Dhaka"
#     post_body['cus_country'] = "Bangladesh"
#     post_body['shipping_method'] = "NO"
#     post_body['multi_card_name'] = ""
#     post_body['num_of_item'] = num_items
#     post_body['product_name'] = "Freelancer Products"
#     post_body['product_category'] = "General"
#     post_body['product_profile'] = "general"


#     response = sslcz.createSession(post_body) # API response
#     # print(response)
#     if response.get("status")=='SUCCESS':
#         return Response({"payment_url":response['GatewayPageURL']})
#     return Response({"error":"Payment initiation failed"},status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def payment_success(request):
#     order_id=request.data.get("tran_id").split('_')[1]
#     order=ServiceOrder.objects.get(id=order_id)
#     order.status="Completed"
#     order.save()
#     return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")

# @api_view(['POST'])
# def payment_cancel(request):
#     return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")

# @api_view(['POST'])
# def payment_fail(request):
#     return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")

@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    order_id = request.data.get("orderId")
    num_items = request.data.get("numItems")

    settings = {
        'store_id':'phima68e538afdcefc',
        'store_pass': 'phima68e538afdcefc@ssl',
        'issandbox': True
    }
    sslcz = SSLCOMMERZ(settings)
    post_body = {
        'total_amount': amount,
        'currency': "BDT",
        'tran_id': f"trx_{order_id}",
        'success_url': f"{main_setting.BACKEND_URL}/api/v1/payment/success/",
        'fail_url': f"{main_setting.BACKEND_URL}/api/v1/payment/fail/",
        'cancel_url': f"{main_setting.BACKEND_URL}/api/v1/payment/cancel/",
        'emi_option': 0,
        'cus_name': f"{user.first_name} {user.last_name}",
        'cus_email': user.email,
        'cus_phone': user.phone_number,
        'cus_add1': user.address,
        'cus_city': "Dhaka",
        'cus_country': "Bangladesh",
        'shipping_method': "NO",
        'multi_card_name': "",
        'num_of_item': num_items,
        'product_name': "Freelancer Products",
        'product_category': "General",
        'product_profile': "general",
    }

    response = sslcz.createSession(post_body)
    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)


from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from orders.models import ServiceOrder
from django.conf import settings as main_setting

# Success
@api_view(['GET', 'POST'])
def payment_success(request):
    tran_id = request.GET.get("tran_id") or request.data.get("tran_id")
    if not tran_id:
        return Response({"error": "Transaction ID missing"}, status=400)

    order_id = tran_id.split('_')[1]
    try:
        order = ServiceOrder.objects.get(id=order_id)
        order.status = "Completed"
        order.save()
    except ServiceOrder.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")

# Fail
@api_view(['GET', 'POST'])
def payment_fail(request):
    return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")

# Cancel
@api_view(['GET', 'POST'])
def payment_cancel(request):
    return HttpResponseRedirect(f"{main_setting.FRONTEND_URL}/dashboard/orders/")


class HasOrderedService(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,service_id):
        user=request.user
        has_Ordered=ServiceOrderItem.objects.filter(order__buyer=user,service_id=service_id).exists()
        return Response({"hasOrdered":has_Ordered})