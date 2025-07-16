

from django.contrib import admin
from financial_options.models import FinantialModels

@admin.register(FinantialModels)
class FinantialModelsAdmin(admin.ModelAdmin):

    list_display = (
        '__str__', 
        'model_type', 
        'usuario', 
        'criado_em', 
    )
    list_filter = ('model_type', 'criado_em', 'usuario')
    search_fields = ('usuario__username', 'model_type')
    date_hierarchy = 'criado_em'