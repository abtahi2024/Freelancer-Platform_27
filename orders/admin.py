from django.contrib import admin
from orders.models import ServiceOrder,ServiceOrderItem, OrderNotification
# Register your models here.
class ServiceOrderItemInline(admin.TabularInline):
    model=ServiceOrderItem
    extra=1
    readonly_fields=['total_price']

class OrderNotificationInline(admin.TabularInline):
    model=OrderNotification
    extra=0
    readonly_fields=['message','created_at','read']



@admin.register(ServiceOrder)
class ServiceAdmin(admin.ModelAdmin):
    list_display= ['id','buyer','status','total_price','created_at']
    list_filter=['status','created_at']
    search_fields=['buyer__email']
    inlines=[ServiceOrderItemInline,OrderNotificationInline]

@admin.register(ServiceOrderItem)
class ServiceOrderItemAdmin(admin.ModelAdmin):
    list_display=['order','service','quantity','price','total_price']
    search_fields=['service__title','order__id']

@admin.register(OrderNotification)
class OrderNotificationAdmin(admin.ModelAdmin):
    list_display=['order','user','message','read','created_at']
    list_filter=['read','created_at']
    search_fields=['user__email','message']