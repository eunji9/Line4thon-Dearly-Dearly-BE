from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.decorators import (api_view, permission_classes, parser_classes)
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from users.models import UserProfile
from .serializers import DirectLetterSerializer
# Create your views here.

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_direct_letter(request):
    from .models import DirectLetter
    serializer = DirectLetterSerializer(
        data = request.data,
        context = {"request":request},
    )
    if serializer.is_valid():
        letter = serializer.save()

        #통계 카운트
        sender_profile,_ = UserProfile.objects.get_or_create(user=letter.sender)
        receiver_profile, _ = UserProfile.objects.get_or_create(user=letter.receiver)

        # 나에게 쓴 편지는 통계에서 제외
        if letter.sender != letter.receiver:
            sender_profile.sent_letter_count += 1
            sender_profile.save(update_fields=["sent_letter_count"])

            receiver_profile.received_letter_count += 1
            receiver_profile.save(update_fields=["received_letter_count"])
        # (sender == receiver일 땐 아무 통계도 증가시키지 않음)

        out_ser = DirectLetterSerializer(letter, context={"request": request})
        return Response(out_ser.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def direct_letter_inbox(request):
    from .models import DirectLetter
    user = request.user
    box = (request.GET.get("box") or "received").lower()
    partner_id = request.GET.get("partner_id")
    sort = (request.GET.get("sort") or "latest").lower()

    if box == "sent":
        qs = DirectLetter.objects.filter(sender=user)
    else:
        qs = DirectLetter.objects.filter(receiver=user)

    if partner_id:
        try:
            partner_id = int(partner_id)
        except ValueError:
            return Response({"detail":"partner_id must be integer"},status=400)
        
        if partner_id == user.id:
            qs = qs.filter(sender=user, receiver=user)
        else:
            if box == "sent":
                qs = qs.filter(receiver_id = partner_id)
            else:
                qs = qs.filter(sender_id=partner_id)

    if sort == "oldest":
        qs=qs.order_by("created_at")
    else:
        qs=qs.order_by("-created_at")
        
    serializer = DirectLetterSerializer(qs, many=True, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def direct_letter_detail(request, id):
    from .models import DirectLetter
    letter = get_object_or_404(DirectLetter, id=id)

    # 나와 무관한 편지 접근 차단
    if letter.sender != request.user and letter.receiver != request.user:
        return Response({"detail": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    serializer = DirectLetterSerializer(letter, context={"request": request})
    return Response(serializer.data, status=status.HTTP_200_OK)