from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """Create and save a User with the given email and password."""
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('The Email Field Must be set')
        email=self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_varified", True)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault('is_varified',True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=true')
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")
        
        return self.create_user(email,password,**extra_fields)