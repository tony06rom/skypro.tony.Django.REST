from users.models import Payments, User
from users.serializers import UserSerializer, PaymentSerializer

from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
