

import uuid
from django.db import models
from django.contrib.auth.models import User

class ModelPadrao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    criado_em = models.DateTimeField('Criado em', auto_now_add=True, help_text='Data da criação do registro')
    alterado_em = models.DateTimeField('Alterado em', auto_now=True, help_text='Data da última alteração no registro')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-criado_em']
        abstract = True
