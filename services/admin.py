from django.contrib import admin
from services.models import Category,Service,Review
# Register your models here.

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Review)