from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import FriendRequest
from .serializers import FriendRequestSerializer, SendFriendRequestSerializer


# 친구 요청 보내기  // body: { "to_user_id": <int> }
@api_view(['POST'])
def send_friend_request(request):
    serializer = SendFriendRequestSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        friend_request = serializer.save()
        return Response(FriendRequestSerializer(friend_request).data,
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 친구 요청 수락
@api_view(['POST'])
def accept_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(
            pk=pk,
            to_user=request.user,
            status=FriendRequest.Status.PENDING
        )
    except FriendRequest.DoesNotExist:
        return Response({'error': '해당 요청이 없거나 이미 처리되었습니다.'},
                        status=status.HTTP_404_NOT_FOUND)

    friend_request.status = FriendRequest.Status.ACCEPTED
    friend_request.responded_at = timezone.now()
    friend_request.save()

    return Response(FriendRequestSerializer(friend_request).data,
                    status=status.HTTP_200_OK)


# 친구 요청 거절
@api_view(['POST'])
def reject_friend_request(request, pk):
    try:
        friend_request = FriendRequest.objects.get(
            pk=pk,
            to_user=request.user,
            status=FriendRequest.Status.PENDING
        )
    except FriendRequest.DoesNotExist:
        return Response({'error': '해당 요청이 없거나 이미 처리되었습니다.'},
                        status=status.HTTP_404_NOT_FOUND)

    friend_request.status = FriendRequest.Status.REJECTED
    friend_request.responded_at = timezone.now()
    friend_request.save()

    return Response(FriendRequestSerializer(friend_request).data,
                    status=status.HTTP_200_OK)


# 받은 친구 요청 목록 조회
@api_view(['GET'])
def received_friend_requests(request):
    qs = FriendRequest.objects.filter(
        to_user=request.user,
        status=FriendRequest.Status.PENDING
    )
    serializer = FriendRequestSerializer(qs, many=True)
    return Response(
        {
            'count': qs.count(),
            'results': serializer.data,
        },
        status=status.HTTP_200_OK
    )