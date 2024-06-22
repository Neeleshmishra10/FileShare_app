from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from files.views import CustomTokenObtainPairView, FileUploadView, UserSignUpView, login_view, home_view, client_home_view, verify_email, FileDownloadView, FileListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('home/', home_view, name='home'),
    path('client_home/', client_home_view, name='client_home'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('verify-email/<str:uidb64>/<str:token>/', verify_email, name='verify_email'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/upload/', FileUploadView.as_view(), name='file_upload'),
    path('download/<int:file_id>/', FileDownloadView.as_view(), name='file_download'),
    path('files/', FileListView.as_view(), name='file_list'),
]


