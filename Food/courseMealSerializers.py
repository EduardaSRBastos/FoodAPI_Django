from rest_framework import serializers
from .models import CourseMealCategory

class CourseMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseMealCategory
        fields = ['id', 'name', 'description']