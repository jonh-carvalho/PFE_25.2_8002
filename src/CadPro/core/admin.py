from django.contrib import admin

from .models import Proposta, Projeto, Relatorio, Entrega, Atividade

# Register your models here.
admin.site.register(Proposta)
admin.site.register(Projeto)
admin.site.register(Relatorio)
admin.site.register(Entrega)
admin.site.register(Atividade)
