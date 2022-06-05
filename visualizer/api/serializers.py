from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from api.models import Analyze


class AnalyzeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyze
        fields = ['id', 'average_rating', 'average_time', 'likes_count',
                  'most_popular_time', 'negative', 'number_of_decanat_replicas',
                  'number_of_student_replicas', 'positive', 'skip', 'speech', 'student']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyze
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {
            'write_only': True,
            'required': True
        }}
