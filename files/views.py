
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser, File
from .serializers import UserSerializer, FileSerializer
from .permissions import IsOpsUser, IsClientUser

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_uploader:
                return redirect('home')
            elif user.is_client:
                return redirect('client_home')
        else:
            return render(request, 'files/login.html', {'error': 'Invalid username or password'})
    return render(request, 'files/login.html')

def home_view(request):
    return render(request, 'files/home.html')

def client_home_view(request):
    return render(request, 'files/client_home.html')

class FileUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsOpsUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        if file_obj.name.endswith(('pptx', 'docx', 'xlsx')):
            file_serializer = FileSerializer(data=request.data)
            if file_serializer.is_valid():
                file_serializer.save(uploaded_by=request.user)
                return Response(file_serializer.data, status=201)
            return Response(file_serializer.errors, status=400)
        else:
            return Response({"error": "Invalid file type"}, status=400)

class UserSignUpView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Send verification 
        verification_url = self.request.build_absolute_uri(f"/verify-email/{urlsafe_base64_encode(force_bytes(user.pk))}")
        send_mail(
            'Verify your email',
            f'Please verify your email by clicking the following link: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return Response({"message": "Verification email sent."}, status=status.HTTP_201_CREATED)

def verify_email(request, uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        user.email_verified = True
        user.save()
        return render(request, 'files/email_verified.html')
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return render(request, 'files/email_not_verified.html')

class FileDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsClientUser]

    def get(self, request, file_id, *args, **kwargs):
        try:
            file = File.objects.get(id=file_id)
            file_path = file.file.path
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
                return response
        except File.DoesNotExist:
            return Response({"error": "File not found"}, status=404)

class FileListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, IsClientUser]
    queryset = File.objects.all()
    serializer_class = FileSerializer
