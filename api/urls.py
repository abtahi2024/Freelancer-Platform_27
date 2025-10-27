from django.urls import path, include
from services.views import CategoryViewSet,ServiceViewSet,ServiceImageViewSet,ReviewViewSet
from rest_framework_nested import routers
from orders.views import ServiceOrderViewSet,initiate_payment,payment_success,payment_cancel,payment_fail
# from users.views import UserViewSet

router=routers.DefaultRouter()
router.register('categories',CategoryViewSet,basename='categories')
router.register('services',ServiceViewSet,basename='services')
router.register('orders',ServiceOrderViewSet,basename='orders')


service_router=routers.NestedDefaultRouter(router,'services',lookup='service')
service_router.register('reviews',ReviewViewSet,basename='service-reviews')
service_router.register('images',ServiceImageViewSet,basename='service-images')


urlpatterns = [

    path('',include(router.urls)),
    path('',include(service_router.urls)),
    # path('',include(user_router.urls)),

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('payment/initiate/',initiate_payment,name='initiate-payment'),
    path('payment/success/',payment_success,name='payment-success'),
    path('payment/cancel/',payment_cancel,name='payment-cancel'),
    path('payment/fail/',payment_fail,name='payment-fail'),
]
