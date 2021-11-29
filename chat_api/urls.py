from django.urls import path
from .views import *

urlpatterns = [
    path('groups/', GroupView.as_view(), name='groups_list'),
    path('groups/detail/<int:pk>/', GroupDetailView.as_view(), name='groups_detail'),
    path('groups/detail/<int:pk>/messages/', GmsView.as_view(), name='group_messages'),
]
