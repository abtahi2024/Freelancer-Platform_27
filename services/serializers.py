from rest_framework import serializers
from services.models import Category,Service,ServiceImage,Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','name','description']

class ServiceImageSerializer(serializers.ModelSerializer):
    image=serializers.ImageField()
    class Meta:
        model = ServiceImage
        fields = ['id', 'image']

class ServiceSerializer(serializers.ModelSerializer):
    seller = serializers.StringRelatedField(read_only=True)  # শুধু email বা str দেখাবে
    category = CategorySerializer(read_only=True)  # nested category
    category_id = serializers.PrimaryKeyRelatedField(        
        queryset=Category.objects.all(), source='category', write_only=True)# write করার সময় category id দিতে হবে
    images = ServiceImageSerializer(many=True, read_only=True)  # nested images

    class Meta:
        model=Service
        fields=['id', 'seller','title','description','price','category','category_id','delivary_time','images','created_at','updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    buyer = serializers.StringRelatedField(read_only=True)  # শুধু email দেখাবে
    images=ServiceImageSerializer(many=True,read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'service', 'buyer', 'rating','images', 'comment', 'created_at']
        read_only_fields=['service','buyer']