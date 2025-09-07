from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator,MaxValueValidator
from services.validators import validate_file_size
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=101)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    seller=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='services')
    title=models.CharField(max_length=200)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='services')
    
    delivary_time=models.PositiveIntegerField(help_text='Estimated delivery time in days')

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering=['-id']
    
    def __str__(self):
        return self.title
    

class ServiceImage(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to="products/images/", validators=[validate_file_size])


class Review(models.Model):
    service=models.ForeignKey(Service,on_delete=models.CASCADE,related_name='reviews')

    buyer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='reviews')

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    comment=models.TextField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service.title or {self.buyer.email}