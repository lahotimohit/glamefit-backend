from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def extract_user_id(token: str):
    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return user_id
    except Exception as e:
        return str(e) 
