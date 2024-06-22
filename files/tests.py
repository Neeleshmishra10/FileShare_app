
import os
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class FileSharingSystemTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_user_login(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_file_upload(self):
        self.client.force_login(self.user) 
        url = reverse('file_upload')
        file_data = SimpleUploadedFile("file.txt", b"file_content")
        data = {
            'file': file_data
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)

    def test_file_download(self):
        self.client.force_login(self.user)  
        upload_url = reverse('file_upload')
        file_data = SimpleUploadedFile("file.txt", b"file_content")
        upload_response = self.client.post(upload_url, {'file': file_data}, format='multipart')
        self.assertEqual(upload_response.status_code, status.HTTP_201_CREATED)
        file_id = upload_response.data['id']
        download_url = reverse('file_download', args=[file_id])
        response = self.client.get(download_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, b"file_content")


# Create your tests here.
