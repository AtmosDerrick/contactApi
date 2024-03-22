import jwt
from rest_framework import authentication,exceptions
from django.conf import settings
from django.contrib.auth.models import User





class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        #get authorization header
        auth_data = authentication.get_authorization_header(request)

        #if user enter no data
        if not auth_data:
            return None
        
        #decode the token into python format
        prefix, token=auth_data.decode('utf-8').split(' ')

        try:

            #valid the token

            #decode the token
            #1. set up a secret key in the settings
            #2. open the .env file and key the secrete key using (os.environ.get('JWT_Secrete_key'))

            #Go to setting and define REST_FRAMEWORK = { }
            #import django.conf import setting in the view


            payload=jwt.decode(token, settings.JWT_SECRET_KEY)

            user=User.objects.get(username=payload['username'])

            return (user, token)

        #if user enter wrong token
        except jwt.DecodeError as identifier:

            #raise an exception / import exception from rest_framework
            raise exceptions.AuthenticationFailed('Your token is invalide, login')
        

            #if token expire
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed('Your token is expired')
        
        return super().authenticate(request) 