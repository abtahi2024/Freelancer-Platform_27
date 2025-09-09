from rest_framework import serializers
from orders.models import ServiceOrder,ServiceOrderItem,OrderNotification
from services.models import Service
from orders.services import ServiceOrderService


class EmptySerializer(serializers.Serializer):
    pass

class SimpleServiceSerializer(serializers.ModelSerializer):# শুধু service এর basic তথ্য দেখাবে।
    class Meta:
        model=Service
        fields=['id','title','price']


class ServiceOrderItemSerializer(serializers.ModelSerializer): #প্রতিটি order item ডিটেইলস।
    service=SimpleServiceSerializer()
    total_price=serializers.SerializerMethodField()

    class Meta:
        model=ServiceOrderItem
        fields=['id','service','quantity','price','total_price']
    
    def get_total_price(self,obj):
        return obj.price*obj.quantity

class ServiceOrderSerializer(serializers.ModelSerializer):
    items = ServiceOrderItemSerializer(many=True, read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = ServiceOrder
        fields = [
            'id', 'buyer', 'buyer_name', 'status',
            'total_price', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['buyer', 'total_price', 'created_at', 'updated_at']


# You need to POST as JSON body.
class CreateServiceOrderSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.DictField(), write_only=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("Order must contain at least one service")
        for item in items:
            if "service_id" not in item:
                raise serializers.ValidationError("Each item must include 'service_id'")
        return items

    def create(self, validated_data):
        buyer = self.context['buyer']  # logged-in user
        services_data = validated_data['items']
        try:
            order = ServiceOrderService.create_order(buyer=buyer, services_data=services_data)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return ServiceOrderSerializer(instance).data


    
class UpdateServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=ServiceOrder
        fields=['status']

class OrderNotificationSerializer(serializers.ModelSerializer):
    order_id=serializers.UUIDField(source='order.id',read_only=True)
    user_email=serializers.EmailField(source='user.email',read_only=True)

    class Meta:
        model=OrderNotification
        fields=['id','order_id','user_email','message','read','created_at']
