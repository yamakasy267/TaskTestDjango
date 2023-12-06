import mock

from django.core.files import File, uploadedfile
from django.core.files.uploadedfile import UploadedFile
from rest_framework.test import APITestCase
from .models import *
from .const import *
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.hashers import make_password


class MyTestApi(APITestCase):

    def setUp(self):
        self.file_mock = mock.MagicMock(spec=File)
        self.file_mock.name = 'photo.jpg'
        user_status = UserStatus.objects.create(status_name=USER_STATUS_ENABLED)
        user_role = Roles.objects.create(role_name=ROLE_USER)
        password = make_password('test')
        user = CustomUser.objects.create(email='test1@mail.ru', password=password, name='test', surname='test',
                                         user_status=user_status, role=user_role,
                                         user_registration_date=datetime.datetime.now())
        file = UsersFiles.objects.create(file_name='photo.jpg', user=user, file=self.file_mock.name)
        user.save()
        self.token = self.test_login()

    def test_registration(self):
        response = self.client.post(reverse('registration'), {
            'email': "test@mail.ru",
            'password': "test",
            'name': 'test',
            'surname': 'test'
        }, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'email': 'test1@mail.ru',
            'password': 'test'
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        key = response.data.get('token').split()
        self.assertEqual(2, len(key))
        self.assertEqual('Token', key[0])
        return key[1]

    def test_upload_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(reverse('upload_file'), {
            'file_name': 'phot',
            'file': UploadedFile(file=self.file_mock)
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(reverse('get_file'), {
            'file_name': 'phot.jpg',
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_put_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(reverse('update_file'), {
            'file_name': 'photo.jpg',
            'file_name_new': 'photo.jpeg',
            'file': UploadedFile(file=self.file_mock)
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_delete_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(reverse('delete_file'), {
            'file_name': 'photo.jpg',
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
