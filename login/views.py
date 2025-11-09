from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .serializers import UserSerializer


def get_tokens_for_user(user):
    """사용자에 대한 JWT 토큰 생성"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@extend_schema(
    summary="현재 로그인한 사용자 정보 조회",
    description="JWT 토큰을 사용하여 현재 로그인한 사용자의 정보를 조회합니다.",
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description="인증 실패 (토큰 없음 또는 만료)"),
    },
    tags=["인증"],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    현재 로그인한 사용자 정보 조회
    GET /auth/user/
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    summary="로그아웃",
    description="JWT Refresh 토큰을 블랙리스트에 추가하여 로그아웃합니다.",
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'JWT Refresh 토큰',
                }
            },
            'required': ['refresh'],
            'example': {
                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
            }
        }
    },
    responses={
        200: OpenApiResponse(
            description="로그아웃 성공",
            examples=[
                OpenApiExample(
                    'Success',
                    value={'message': '로그아웃 성공'}
                )
            ]
        ),
        400: OpenApiResponse(description="로그아웃 실패 (잘못된 토큰)"),
        401: OpenApiResponse(description="인증 실패"),
    },
    tags=["인증"],
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    로그아웃 (JWT 토큰 블랙리스트 처리)
    POST /auth/logout/
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response(
            {"message": "로그아웃 성공"},
            status=status.HTTP_200_OK
        )
    
    except Exception as e:
        return Response(
            {"error": "로그아웃 실패"},
            status=status.HTTP_400_BAD_REQUEST
        )


@extend_schema(
    summary="카카오 로그인 콜백 - JWT 토큰 발급",
    description="""
    카카오 로그인이 성공한 후 호출되는 엔드포인트입니다.
    
    **사용 방법:**
    1. `/accounts/kakao/login/` 으로 접속하여 카카오 로그인 시작
    2. 카카오 인증 완료 후 `/accounts/kakao/login/callback/` 으로 자동 리다이렉트
    3. 이 엔드포인트(`/auth/kakao/callback/`)에서 JWT 토큰 발급
    
    **주의:** 이 API는 Swagger에서 직접 테스트하기 어렵습니다. 
    실제 카카오 로그인 플로우를 통해서만 정상 작동합니다.
    """,
    responses={
        200: OpenApiResponse(
            description="카카오 로그인 성공 및 JWT 토큰 발급",
            examples=[
                OpenApiExample(
                    'Success',
                    value={
                        "message": "카카오 로그인 성공",
                        "tokens": {
                            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                        },
                        "user": {
                            "id": 1,
                            "username": "kakao_123456789",
                            "email": "user@example.com"
                        }
                    }
                )
            ]
        ),
        401: OpenApiResponse(description="로그인 실패"),
    },
    tags=["카카오 로그인"],
)
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_login_callback(request):
    """
    카카오 로그인 성공 후 JWT 토큰 반환
    GET /accounts/kakao/login/callback/ 후 자동 호출
    """
    user = request.user
    
    if user.is_authenticated:
        tokens = get_tokens_for_user(user)
        user_data = UserSerializer(user).data
        
        return Response({
            "message": "카카오 로그인 성공",
            "tokens": tokens,
            "user": user_data
        }, status=status.HTTP_200_OK)
    
    return Response(
        {"error": "로그인 실패"},
        status=status.HTTP_401_UNAUTHORIZED
    )
