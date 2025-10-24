from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from users.models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = [
            'id',
            'email',
            'password',
            'first_name',
            'last_name',
            'role',
            'address',
            'phone_number',
            'bio',
        ]

class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        ref_name = 'CustomUser'
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'is_varified',
            'address',
            'phone_number',
            'bio',
            'is_staff',
        ]
        read_only_fields=['is_staff']
