from django.urls import path
from .views import *

urlpatterns = [
    path('groups/', GroupView.as_view(), 'groups_list'),
    path('groups/detail/<int:pk>/', GroupDetailView.as_view(), 'groups_detail'),
]
