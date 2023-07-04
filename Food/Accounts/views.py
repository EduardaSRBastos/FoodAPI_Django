from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..utils import generate_token


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='User created.'),
    }
)

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        return Response({'message': 'Registration successful.'}, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='User logged in.'),
    }
)

@api_view(['POST'])
@ensure_csrf_cookie
def userLogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        token = generate_token(user)
        return Response({'message': 'Login successful.', 'token': token})
    else:
        # Handle invalid login credentials
        return Response({'message': 'Invalid login credentials.'}, status=401)


@api_view(['POST'])
@ensure_csrf_cookie
def userLogout(request):
    logout(request)
    return Response({'message': 'Logout successful.'})
