from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """사용자 프로필 정보"""
    class Meta:
        model = UserProfile
        fields = ['nickname', 'profile_image', 'created_letterroom_count', 
                  'sent_letter_count', 'received_letter_count']


class UserSerializer(serializers.ModelSerializer):
    """사용자 기본 정보 + 프로필"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile']
        read_only_fields = ['id', 'username', 'email']

