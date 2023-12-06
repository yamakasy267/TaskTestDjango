from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from .models import CustomUser, Roles, UserStatus, UsersFiles
from .const import *
from rest_framework.validators import UniqueValidator
import datetime
import jwt
from Test import settings


class RegistrationSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'surname', 'email', 'password']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        user = CustomUser.objects.create(**validated_data, user_registration_date=timezone.now(),
                                         role=Roles.objects.get(role_name=ROLE_USER),
                                         user_status=UserStatus.objects.get(status_name=USER_STATUS_ENABLED))
        return user


class AuntificationSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def JWTAuth(self, validated_data):
        try:
            user = CustomUser.objects.get(email=validated_data['email'])
            cheked_pass = check_password(validated_data['password'], user.password)
            if not cheked_pass:
                raise Exception("dont valid email or password")
        except Exception as e:
            raise e
        dt = datetime.datetime.now() + datetime.timedelta(days=1)
        print(dt)
        token = jwt.encode({
            'id': user.pk,
            'exp': int(dt.timestamp())},
            key=settings.SECRET_KEY)

        return token


class UploadFileSerializers(serializers.ModelSerializer):
    class Meta:
        model = UsersFiles
        fields = '__all__'


class UpdateFileSerializers(serializers.ModelSerializer):
    file_name_new = serializers.CharField(required=False)
    file = serializers.FileField(required=False)

    class Meta:
        model = UsersFiles
        fields = ['file_name_new', 'file']

    def update(self, instance, validated_data):
        if validated_data.get('file_name_new'):
            instance.file_name = validated_data['file_name_new']
        if validated_data.get('file'):
            instance.file = validated_data['file']
        instance.save()
        return instance
