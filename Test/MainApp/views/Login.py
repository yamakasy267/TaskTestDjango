from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import AuntificationSerializers
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR
)
logger = logging.getLogger(__name__)


class Login(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = AuntificationSerializers

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "file_name": openapi.Schema(type=openapi.TYPE_STRING, description="file_name")}),
        consumes=['application/json'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'token': openapi.Schema(type=openapi.TYPE_STRING,
                                    description="сначало идет ключ-слово Token потом сам токен",
                                    pattern="Token 12-094ioino9832y4")
        }),
                   500: "Server error"},
        operation_description=f'''Апи для входа'''
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = {**serializer.validated_data, **kwargs}
        try:
            return Response(status=200, data={'token': f"Token {serializer.JWTAuth(validated_data)}"})
        except Exception as e:
            logger.error(f'ERROR -> failed authorization because: {e}')
            return Response(status=500)
