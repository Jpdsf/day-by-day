from rest_framework import serializers
from accounts.models.user import UserDay

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = UserDay
        fields = ['username', 'email', 'password', 'password2', 'bio', 'goals']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserDay.objects.create_user(**validated_data)
        return user