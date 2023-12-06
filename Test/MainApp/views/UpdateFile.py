from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..serializers import UpdateFileSerializers
from ..Authorization import JWTAuthorization
from ..models import UsersFiles
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class UpdateFile(generics.GenericAPIView, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthorization]
    serializer_class = UpdateFileSerializers

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(name="Token", in_="header", type=openapi.IN_HEADER,required=True,
                                             description="Токен поссылается в заголовках, в поле Authorization в виде Token (сам токен)")],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, required=['file_name'], properties={
            "file_name": openapi.Schema(type=openapi.TYPE_STRING, description="file_name"),
            "file_name_new": openapi.Schema(type=openapi.TYPE_STRING, description="file_name_new"),
            "file": openapi.Schema(type=openapi.TYPE_FILE, description="file")}),
        consumes=['application/json'],
        responses={200: 'OK',
                   401: "Permission denied",
                   500: "Server error"},
        operation_description=f'''Апи для обновления файла'''
    )
    def put(self, request, *args, **kwargs):
        file_name = request.data.get('file_name')
        if not file_name:
            return Response(status=400, data={'error': "Field file_name required"})
        try:
            instance = UsersFiles.objects.get(user=request.user, file_name=file_name)
        except Exception as e:
            logger.error(f"ERROR -> Failed get file because {e}")
            return Response(status=500, data={'error': "Failed get file"})
        serializer = self.serializer_class(data=request.data, instance=instance)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            logger.error(f"ERROR UPDATE FILE -> {e}")
            return Response(status=500, data={'error': "failed update file"})
        return Response(status=200)
