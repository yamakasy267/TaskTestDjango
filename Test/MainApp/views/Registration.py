from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import RegistrationSerializers, AuntificationSerializers
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class Registration(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializers

    @swagger_auto_schema(
        request_body=RegistrationSerializers,
        consumes=['application/json'],
        responses={200: 'OK',
                   500: "Server error"},
        operation_description=f'''Апи для регистрации'''
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"ERROR REGISTRATION -> {e}")
            return Response(status=500, data={'error': "failed registration"})

        return Response(status=200)
