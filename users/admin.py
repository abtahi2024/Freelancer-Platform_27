from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
    model=User
    list_display=('email','id','role','is_varified','is_active','is_staff')
    list_filter=('role','is_varified', 'is_active', 'is_staff')

    fieldsets=(
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'address', 'phone_number', 'bio')}),
        ('Role & Verification', {'fields': ('role', 'is_varified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_varified', 'is_staff', 'is_active'),
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User,CustomUserAdmin)