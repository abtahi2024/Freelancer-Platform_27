from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.filters import SearchFilter,OrderingFilter
from services.filtes import ServicesFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from services.models import Category,Service,ServiceImage,Review
from services.serializers import CategorySerializer,ServiceSerializer,ServiceImageSerializer,ReviewSerializer
from services.paginations import DefaultPagination
from api.permissions import IsAdminOrReadOnly
from services.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class CategoryViewSet(ModelViewSet):
    """
    API endpoint for managing Categories
    - Admins can create, update, and delete categories
    - Users can view category list and details
    """
    queryset=Category.objects.annotate(service_count=Count('services')).all()
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    permission_classes=[IsAdminOrReadOnly]

    @swagger_auto_schema(
        operation_summary='List all Categories',
        operation_description='Retrieve all Catagories with their service count',
        responses={
            200:
            CategorySerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve Category Details',
        responses={
            200: CategorySerializer
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a new Category (Admin only)',
        request_body=CategorySerializer,
        responses={
            201:
            CategorySerializer,
            400:"Bed request"
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Partially update Category',
        request_body=CategorySerializer,
        responses={
            200:CategorySerializer
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='PUT the category',
        operation_description='This is update Category',
        request_body=CategorySerializer,
        responses={
            200:'Category update',
            400: 'Bed request'
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Delete a Catagory only Admin',
        responses={
            204: 'Categoryes succeessfully Deleted'
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class ServiceViewSet(ModelViewSet):
    """
    API endpoint for managing freelance services
     - Sellers can create, update, and delete their services
     - Buyers can browse, search, filter, and order by price
    """
    queryset=Service.objects.all()
    serializer_class=ServiceSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_class=ServicesFilter
    pagination_class=DefaultPagination
    search_fields=['title','description']
    ordering_fields=['price','updated_at']
    permission_classes=[IsAuthenticatedOrReadOnly]
    # permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        return Service.objects.prefetch_related('images','reviews').all()
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user) 

    @swagger_auto_schema(
            operation_summary='List all Services',
            operation_description='Get a Pageinated list of service with filtering searching, and ordering',
            responses={
                200:
                ServiceSerializer(many=True)
            },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a service by (Admin only)",
        operation_description='This Allow an Admin to create a Service',
        request_body=ServiceSerializer,
        responses={
            201:ServiceSerializer,
            400:"Bed request"
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Retrieve id details',
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Partial update service only Admin'

    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Admins only can update'
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class ServiceImageViewSet(ModelViewSet):
    serializer_class=ServiceImageSerializer
    permission_classes=[IsAuthenticatedOrReadOnly]
    permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        return ServiceImage.objects.filter(service_id=self.kwargs.get('service_pk'))
    
    def perform_create(self, serializer):
        return serializer.save(service_id=self.kwargs.get('service_pk'))
    
    @swagger_auto_schema(
        operation_summary='List service images',
        operation_description='Retrieve all images for a specific Service',
        responses={
            200:ServiceImageSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Upload a new service image (Admin only)',
        request_body=ServiceImageSerializer,
        responses={
            201:
            ServiceImageSerializer,
            400: 'Bed request'
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ReviewViewSet(ModelViewSet):
    serializer_class=ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsReviewAuthorOrReadonly]

    # permission_classes=[IsAdminOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(service_id=self.kwargs.get('service_pk'))
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user,service_id=self.kwargs['service_pk'])
    
    def perform_update(self, serializer):
        return serializer.save()
    
    def get_serializer_context(self):
        return {'service_id': self.kwargs.get('service_pk')}
    
    @swagger_auto_schema(
        operation_summary='List reviews for a service',
        responses={
            200: ReviewSerializer(many=True)
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary='Create a review',
        operation_description='Authenticated user can create a review for a service',
        request_body=ReviewSerializer,
        responses={
            201:
            ReviewSerializer,
            400:'Bed Request'
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
