from rest_framework.generics import ListAPIView,CreateAPIView
from django.contrib.auth import get_user_model
from .serializers import ListEmployeeSerializer, HireEmployeeSerializer, \
                            AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .permissions import IsHRManager
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled


class EmployeesListView(ListAPIView):
    """Lists and retrieves Employee objects"""
    queryset = get_user_model().objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated, IsHRManager]
    throttle_classes = []
    serializer_class = ListEmployeeSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class HireEmployeeView(CreateAPIView):
    serializer_class = HireEmployeeSerializer
    permission_classes = [IsHRManager]
    throttle_classes = []
    fields = ['name', 'email', 'password', 'position']

class Attendance(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated,]
    throttle_classes = [UserRateThrottle]

    def get(self, request, format=None):
        request.user.attendance = request.user.attendance+1
        request.user.save()
        return Response(f'Hello, {request.user.name}! Have a good day at work!')

    def throttled(self, request, wait):
        raise Throttled(detail={
              "message":"You can only attend once per day",
        })
