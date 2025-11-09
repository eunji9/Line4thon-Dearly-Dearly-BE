from django.urls import path, include
from . import views

urlpatterns = [
    # 현재 사용자 정보 조회
    path('auth/user/', views.current_user, name='current-user'),
    
    # 로그아웃
    path('auth/logout/', views.logout, name='logout'),
    
    # 카카오 로그인 성공 후 JWT 토큰 발급
    path('auth/kakao/callback/', views.kakao_login_callback, name='kakao-callback'),
    
    # 카카오 로그인 (django-allauth 직접 사용)
    # GET /accounts/kakao/login/ - 카카오 로그인 시작
    # GET /accounts/kakao/login/callback/ - 카카오 콜백 (자동으로 로그인 처리)
    path('accounts/', include('allauth.urls')),
]

