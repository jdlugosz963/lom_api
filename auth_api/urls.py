from django.urls import path
from knox import views as knox_views
from .views import LoginView, RegisterView, UserInfo


urlpatterns = [
     path('login/', LoginView.as_view(), name='login'),
     path('register/', RegisterView.as_view(), name='register'),
     path('info/', UserInfo.as_view(), name='info'),
     path('logout/', knox_views.LogoutView.as_view(), name='logout'),
     path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
]
