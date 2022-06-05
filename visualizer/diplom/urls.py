
from django.contrib import admin
from django.urls import path, include

# from api.views import index
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', include('api.urls')),
    path('admin/', admin.site.urls),
    path('auth/', obtain_auth_token),
    path("accounts/", include("django.contrib.auth.urls"))
]
