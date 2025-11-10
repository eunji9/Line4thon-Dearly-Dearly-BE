from django.urls import path
from . import views

urlpatterns = [
    # FriendRequest
    path("requests", views.send_friend_request),                        # 친구 요청 보내기
    path("requests/received", views.received_friend_requests),          # 받은 요청 목록 조회
    path("requests/<int:pk>/accept", views.accept_friend_request),      # 친구 요청 수락
    path("requests/<int:pk>/reject", views.reject_friend_request),      # 친구 요청 거절
]