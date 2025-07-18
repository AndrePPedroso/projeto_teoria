
import os
from core.models import ModelPadrao
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

def _get_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    timestamp_str = instance.criado_em.strftime('%Y-%m-%d_%H-%M-%S')
    new_filename = f"{instance.model_type}_{timestamp_str}.{ext}"
    return os.path.join('financial_reports', instance.usuario.username, new_filename)

class FinantialModelsChoices(models.TextChoices):
    BLACK_SCHOLES = 'BLACK_SCHOLES', _('Black-Scholes'),
    BLACK_SCHOLES_MERTON = 'BLACK_SCHOLES_MERTON', _('Black-Scholes-Merton'),
    GENERALIZED_BLACK_SCHOLES_MERTON = 'GENERALIZED_BLACK_SCHOLES_MERTON', _('Generalized Black-Scholes-Merton'),
    COX_ROSS = 'COX_ROSS', _('Cox-Ross Binomial'),

class FinantialModels(ModelPadrao):
    model_type = models.CharField(max_length=100, blank=True, null=True, choices=FinantialModelsChoices.choices)
    parameters = models.JSONField(
        default=dict,
        verbose_name="Simulation Parameters",
        help_text="All input parameters for the simulation"
    )

    results = models.JSONField(
        default=dict,
        verbose_name="Simulation Results",
        help_text="All calculated results from the simulation"
    )

    report = models.FileField(
        upload_to=_get_upload_path,
        null=True,
        blank=True,
        verbose_name="PDF Report",
        validators=[FileExtensionValidator(['pdf'])]
    )

    class Meta:
        abstract = False
        verbose_name = "Financial Simulation"
        verbose_name_plural = "Financial Simulations"
    
    def __str__(self):
        return f"{self.usuario or 'Unnamed'},{self.model_type} ({self.criado_em.date()})"