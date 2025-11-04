from django.urls import path
from .views import dilema_do_prisioneiro_view

urlpatterns = [
    path('dilema-do-prisioneiro/', dilema_do_prisioneiro_view, name='dilema_do_prisioneiro'),
]
