from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import UploadFileSerializers
from ..Authorization import JWTAuthorization
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class UploadFile(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthorization]
    serializer_class = UploadFileSerializers

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(name="Token", in_="header", type=openapi.IN_HEADER, required=True,
                                             description="Токен поссылается в заголовках, в поле Authorization в виде Token (сам токен)")],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'file_name': openapi.Schema(type=openapi.TYPE_STRING, description="name file"),
            'file': openapi.Schema(type=openapi.TYPE_FILE, description='file')
        }),
        consumes=['application/json'],
        responses={200: 'OK',
                   401: "Permission denied",
                   500: "Server error"},
        operation_description=f'''Апи для загрузки файла'''
    )
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['user'] = request.user.pk
        request.data._mutable = False
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"ERROR UPLOAD FILE -> {e}")
            return Response(status=500, data={'error': "failed upload file"})
        return Response(status=200)
