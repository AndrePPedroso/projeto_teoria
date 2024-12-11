
from django.contrib import admin
from django.urls import path , include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title='teoria',
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/login/", custom_admin_login),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), 
    path('api/swagger.<slug:format>)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("home/", home_view, name="home"),
    path('teoria/', include('teoria_opcao.urls')),  
    path('estocasticos/', include('estocasticos.urls')),  
    path('set_language/', set_language, name='set_language'),
]