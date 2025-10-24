from django.contrib import admin
from services.models import Category,Service,Review,ServiceImage
# Register your models here.

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(ServiceImage)
admin.site.register(Review)