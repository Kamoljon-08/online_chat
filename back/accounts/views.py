from django.contrib.auth import login

from .permissions import IsAuthorOrReadOnly

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView

from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer, UserSerializerAll

from django.views.decorators.debug import sensitive_post_parameters

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
# from django.contrib.auth.models import User
from .models import UserModel

from rest_framework.permissions import IsAuthenticated

from knox.models import AuthToken
from rest_framework import status
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

class AuthTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

class LoginAPI(APIView):
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(username=serializer.data['email'], password=request.data['password'])
            if user is not None:
                login(request, user)
                return Response({'token': AuthToken.objects.create(user)[1]})
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# accounts/views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .utils import generate_otp, send_otp_email
# from .models import UserModel

# class LoginWithOTP(APIView):
#     def post(self, request):
#         email = request.data.get('email', '')
#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         otp = generate_otp()
#         user.otp = otp
#         user.save()

#         send_otp_email(email, otp)
#         # send_otp_phone(phone_number, otp)

#         return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)


# # accounts/views.py

# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token

# class ValidateOTP(APIView):
#     def post(self, request):
#         email = request.data.get('email', '')
#         otp = request.data.get('otp', '')

#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

#         if user.otp == otp:
#             user.otp = None  # Reset the OTP field after successful validation
#             user.save()

#             # Authenticate the user and create or get an authentication token
#             token, _ = Token.objects.get_or_create(user=user)

#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)

# Register Api
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
})

# Get User Api
class UserAPI(generics.ListAPIView):
    permissions_class = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()

class UserDetailAPI(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializerAll
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

class UserUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializerAll
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

class UserDeleteAPI(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializerAll
    queryset = UserModel.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

# Change Password API
class ChangePasswordView (generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    models = UserModel
    permissions_class = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update (self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['Wrong Password !']}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonView(generics.ListAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id', 'username')
    search_fields = ('id', 'username')