from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Notification
from .serializers import NotificationSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_list(request):
    #내 알림 목록 
    qs = Notification.objects.filter(user=request.user)
    if request.query_params.get("unread_only") == "true":
        qs = qs.filter(is_read=False)

    serializer = NotificationSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_read(request, pk):
    #알림 하나 읽음 처리
    try:
        noti = Notification.objects.get(pk=pk, user=request.user)
    except Notification.DoesNotExist:
        return Response({"detail": "알림이 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    noti.is_read = True
    noti.save(update_fields=["is_read"])
    return Response({"detail": "ok"}, status=status.HTTP_200_OK)
