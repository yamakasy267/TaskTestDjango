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


class DeleteFile(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthorization]

    @swagger_auto_schema(
        manual_parameters=[openapi.Parameter(name="Token", in_="header", type=openapi.IN_HEADER,required=True,
                                             description="Токен поссылается в заголовках, в поле Authorization в виде Token (сам токен)")],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "file_name": openapi.Schema(type=openapi.TYPE_STRING, description="file_name")}),
        consumes=['application/json'],
        responses={200: "OK",
                   401: "Permission denied",
                   500: "Server error"},
        operation_description=f'''Апи для удаления файла'''
    )
    def delete(self, request, *args, **kwargs):
        file_name = request.data.get('file_name')
        if not file_name:
            return Response(status=400, data={'error': "Field file_name required"})
        try:
            file = UsersFiles.objects.get(user=request.user, file_name=file_name)
            file.delete()
        except Exception as e:
            logger.error(f"ERROR -> Failed deleted file because {e}")
            return Response(status=500, data={'error': "Failed deleted file"})
        return Response(status=200)
