from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..utils import generate_token, validate_token
from django.views.decorators.csrf import ensure_csrf_cookie

# Factory Pattern
class UserFactory:
    @staticmethod
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return user
        return None

    @staticmethod
    def create_serializer(user):
        return UserSerializer(user)

# Strategy Pattern
class AuthenticationStrategy:
    def authenticate(self, request, **kwargs):
        raise NotImplementedError

class UsernamePasswordAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, request, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        return authenticate(request, username=username, password=password)

class TokenAuthenticationStrategy(AuthenticationStrategy):
    def authenticate(self, request, **kwargs):
        # Retrieve and validate the token from the request
        token = kwargs.get('token')
        user = validate_token(token)
        return user



@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='User created.'),
    }
)

@api_view(['POST'])
def register(request):
    user_factory = UserFactory()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = user_factory.create_user(request.data)
        if user is not None:
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
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Strategy Pattern
    authentication_strategy = UsernamePasswordAuthenticationStrategy()
    user = authentication_strategy.authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        token = generate_token(user)
        return Response({'message': 'Login successful.', 'token': token})
    else:
        return Response({'message': 'Invalid login credentials.'}, status=401)

@api_view(['POST'])
@ensure_csrf_cookie
def user_logout(request):
    logout(request)
    return Response({'message': 'Logout successful.'})
