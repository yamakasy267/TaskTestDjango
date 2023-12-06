from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..Authorization import JWTAuthorization
import logging
from ..models import UsersFiles

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class GetFile(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthorization]

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(name="Token", in_="header", type=openapi.IN_HEADER, required=True,
                                             description="Токен поссылается в заголовках, в поле Authorization в виде Token (сам токен)"),
                           openapi.Parameter(name="file_name", in_="query", type=openapi.TYPE_STRING,
                                             description="необезательный параметр, если нужно получить 1 файл")],
        consumes=['application/json'],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'files': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'file_name': openapi.Schema(type=openapi.TYPE_STRING, description='file name'),
                'file': openapi.Schema(type=openapi.TYPE_FILE, description='file')
            }, description="если было отправлено file_name, то придет file, иначе придет массив file_name и file"))
        }),
                   401: "Permission denied",
                   500: "Server error"},
        operation_description=f'''Апи для получения файла'''
    )
    def get(self, request, *args, **kwargs):
        file_name = request.data.get('file_name')
        if not file_name:
            file = UsersFiles.objects.filter(user=request.user).values("file_name", "file")
        else:
            try:
                file = {'file': str(UsersFiles.objects.get(user=request.user, file_name=file_name).file)}
            except Exception as e:
                logger.error(f"ERROR -> Not found file because {e}")
                return Response(status=500, data={'error': "Not found file"})
        return Response(status=200, data={'files': file})
