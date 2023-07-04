from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Group.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'roles')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])

        user = User.objects.create_user(**validated_data)

        for role_name in roles_data:
            role, _ = Group.objects.get_or_create(name=role_name)
            user.groups.add(role)

        return user