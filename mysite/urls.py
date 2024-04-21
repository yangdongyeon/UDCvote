# mysite/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),  # 'myapp'은 앱의 이름이므로 실제로 사용하는 앱 이름으로 변경하세요.
    path('user/login/', auth_views.LoginView.as_view(), name='login'),  # 로그인 URL 추가
    path('user/logout/', auth_views.LogoutView.as_view(), name='logout'),  # 로그아웃 URL 추가
]

