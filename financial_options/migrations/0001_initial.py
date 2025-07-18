# Generated by Django 4.2 on 2025-07-13 19:41

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FinantialModels',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True, help_text='Data da criação do registro', verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, help_text='Data da última alteração no registro', verbose_name='Alterado em')),
                ('model_type', models.CharField(blank=True, choices=[('BLACK_SCHOLES', 'Black-Scholes'), ('BLACK_SCHOLES_MERTON', 'Black-Scholes-Merton'), ('GENERALIZED_BLACK_SCHOLES_MERTON', 'Generalized Black-Scholes-Merton'), ('COX_ROSS', 'Cox-Ross Binomial')], max_length=100, null=True)),
                ('parameters', models.JSONField(default=dict, help_text='All input parameters for the simulation', verbose_name='Simulation Parameters')),
                ('results', models.JSONField(default=dict, help_text='All calculated results from the simulation', verbose_name='Simulation Results')),
                ('report', models.FileField(blank=True, null=True, upload_to='financial_reports/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='PDF Report')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Financial Simulation',
                'verbose_name_plural': 'Financial Simulations',
                'abstract': False,
            },
        ),
    ]
