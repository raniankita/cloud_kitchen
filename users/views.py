from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .tasks import send_welcome_email

from .serializers import * 

# Create your views here.
class SignupAPIView(APIView):
    def post(self,request):
        serializer = UserSignupSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_welcome_email.delay(user.email, user.username)

            return Response({"message":"User Registered successfully."}, status= status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    


class CustomLoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.get_user(request.data.get("username"))
        
        if user:
            response.data['user'] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "is_customer": user.is_customer,
                "is_kitchen": user.is_kitchen,
                "is_delivery_agent": user.is_delivery_agent
            }
        return response

    def get_user(self, username):
        User = get_user_model()
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)

        except TokenError:
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)