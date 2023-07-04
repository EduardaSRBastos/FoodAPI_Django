from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import get_user_model

User = get_user_model()

def generate_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
        # Add more custom claims as needed
    }
    token = AccessToken.for_user(user)
    token.payload.update(payload)
    return str(token)

def validate_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        # Retrieve the user based on the user_id from the token
        user = User.objects.get(id=user_id)
        return user
    except (TokenError, User.DoesNotExist):
        return None
