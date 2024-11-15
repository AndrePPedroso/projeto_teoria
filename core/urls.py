
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
    path('', include('usuario.urls')),
    #------pages---------------
    path('processos-home/', processos_home, name='processos_home'),
    path('teoria-opcoes-financeiras/', teoria_opcoes_financeiras, name='teoria_opcoes_financeiras'),
    path('teoria-opcoes-reais/', teoria_opcoes_reais, name='teoria_opcoes_reais'),
    path('cadeia-markov/', cadeia_markov, name='cadeia_markov'),
    path('random_walk_normal/', random_walk_normal, name='random_walk_normal'),
    path('random_walk/', random_walk, name='random_walk'),
    #------calculos----------
    path('markov_simulador/', markov_simulator, name='simulate_markov'),
    path('random_walk_normal_simulador/', random_walk_normal_view, name='simulate_random_walk_normal'),
    path('random_walk_simulador/', random_walk_view, name='simulate_random_walk'),
]