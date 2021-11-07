from django.contrib import admin
from knox.models import AuthToken

admin.register(AuthToken)
