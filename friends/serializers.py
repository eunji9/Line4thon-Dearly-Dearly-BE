from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest

User = get_user_model()


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user_username = serializers.CharField(source='from_user.username', read_only=True)
    to_user_username = serializers.CharField(source='to_user.username', read_only=True)

    class Meta:
        model = FriendRequest
        fields = [
            'id',
            'from_user',
            'from_user_username',
            'to_user',
            'to_user_username',
            'status',
            'created_at',
            'responded_at',
        ]
        read_only_fields = ['from_user', 'status', 'created_at', 'responded_at']


class SendFriendRequestSerializer(serializers.Serializer):
    to_user_id = serializers.IntegerField()

    def validate(self, attrs):
        request = self.context['request']
        from_user = request.user
        to_user_id = attrs['to_user_id']

        if from_user.id == to_user_id:
            raise serializers.ValidationError("자기 자신에게 친구 요청을 보낼 수 없습니다.")

        # 대상 유저 존재 여부 확인
        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("해당 유저를 찾을 수 없습니다.")

        # 이미 대기중인 요청 있는지 확인
        if FriendRequest.objects.filter(
            from_user=from_user,
            to_user=to_user,
            status=FriendRequest.Status.PENDING
        ).exists():
            raise serializers.ValidationError("이미 친구 요청을 보냈습니다.")

        attrs['to_user'] = to_user
        return attrs

    def create(self, validated_data):
        from_user = self.context['request'].user
        to_user = validated_data['to_user']
        return FriendRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
        )