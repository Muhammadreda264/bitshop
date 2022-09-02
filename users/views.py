from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from users.serializers import UserSerializer, LoginSerializer
from rest_framework import views


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.",
        })


class LoginView(generics.GenericAPIView):
    """
            This endpoint requires two fields for authentication:
              * username
              * password.
            It will try to authenticate the user with when validated.
    """
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
                                     context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)
