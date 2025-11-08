from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

# Create your views here.
class UserProfileView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): #현재 로그린 한 유저 프로필 반환
        return UserProfile.objects.get(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        #patch 요청시 프로필 부분 수정(닉네임만/이미지만)가능
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)