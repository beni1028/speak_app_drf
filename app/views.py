# views.py
import requests

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.conf import settings


from .serializers import UserSerializer, AuthTokenSerializer
from .models import User
from .tasks import send_activation_email


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    '''
    '''
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    send_activation_email(user.email)
    send_activation_email.delay(user.email)
    return Response({"messsage":"SignUp Successful. Please check you email for the activation link"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_token(request):
    '''
    '''
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(data=serializer.validated_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_account(request):
    if request.query_params.get("aid",None):
        # Can add better validation to restrcit reuse of link
        if User.objects.filter(aid=request.query_params['aid'],is_active=True).exists():
            return Response({'message': 'Invalid url.'}, status=status.HTTP_400_BAD_REQUEST) 
        
        User.objects.filter(aid=request.query_params['aid']).update(is_active=True)
        return Response({'message': 'Account activated successfully'}, status=status.HTTP_200_OK)
    return Response({'message': 'Invalid url. Please request for a new ID'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verifiction(request):
    if not request.data.get("email",None):
        return Response({'message': 'Email is needed'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=request.data["email"])
    except User.DoesNotExist:
        return Response({'message': 'Please provide a valid email.'}, status=status.HTTP_400_BAD_REQUEST)

    if user.is_active:
        return Response({'message': 'This user has alrady been activated.'}, status=status.HTTP_400_BAD_REQUEST)

    send_activation_email(user.email)
    send_activation_email.delay(user.email)

    return Response({'message': f'Activatin email sent to {user.email}'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_weather_data(request):
    country = request.GET.get('country')
    city = request.GET.get('city')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={settings.WEATHER_API_KEY}'
    response = requests.get(url)
    print(response.json())
    if response.status_code == 200:
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    print()
    return Response({'error': 'Unable to fetch weather data'}, status=status.HTTP_400_BAD_REQUEST)
