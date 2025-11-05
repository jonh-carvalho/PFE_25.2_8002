from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('comunidade', 'Comunidade Externa'),
        ('coordenador', 'Coordenador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('admin', 'Administrador'),
    ]

    tipo_usuario: models.CharField = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='comunidade'
    )
    telefone: models.CharField = models.CharField(max_length=20, blank=True)
    organizacao: models.CharField = models.CharField(
        max_length=100, blank=True
    )
    data_registro: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"


class Proposta(models.Model):
    STATUS_CHOICES = [
        ('enviada', 'Enviada'),
        ('em_analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    titulo: models.CharField = models.CharField(max_length=200)
    descricao: models.TextField = models.TextField()
    problema_resolver: models.TextField = models.TextField()
    publico_alvo: models.TextField = models.TextField()
    relevancia_social: models.TextField = models.TextField()
    # Removemos os campos de contato individuais pois agora usamos o usuário
    usuario: models.ForeignKey = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name='propostas'
    )
    status: models.CharField = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='em_analise'
    )
    data_submissao: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )
    documentos: models.FileField = models.FileField(
        upload_to='documentos_propostas/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.titulo


# Os outros modelos (Projeto, Relatorio, Atividade, Entrega) permanecem os mesmos
# mas atualizamos o campo professor_responsavel para ForeignKey
class Projeto(models.Model):
    STATUS_CHOICES = [
        ('em_execucao', 'Em Execução'),
        ('concluido', 'Concluído'),
        ('suspenso', 'Suspenso'),
    ]

    titulo: models.CharField = models.CharField(max_length=200)
    descricao: models.TextField = models.TextField()
    objetivos: models.TextField = models.TextField()
    impacto_esperado: models.TextField = models.TextField()
    status: models.CharField = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='em_execucao'
    )
    data_inicio: models.DateField = models.DateField()
    data_termino_prevista: models.DateField = models.DateField(null=True, blank=True)
    data_conclusao: models.DateField = models.DateField(null=True, blank=True)
    proposta_origem: models.OneToOneField = models.OneToOneField(
        Proposta,
        on_delete=models.CASCADE,
        related_name='projeto_gerado'
    )
    professor_responsavel: models.ForeignKey = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'tipo_usuario': 'professor'},
        related_name='projetos_como_professor'
    )
    
    def __str__(self):
        return self.titulo

# Atualizar outros modelos para usar ForeignKey onde necessário...


class Relatorio(models.Model):
    projeto: models.ForeignKey = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='relatorios')
    titulo: models.CharField = models.CharField(max_length=200)
    conteudo: models.TextField = models.TextField()
    data_relatorio: models.DateField = models.DateField()
    data_criacao: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    arquivo: models.FileField = models.FileField(upload_to='relatorios/', blank=True, null=True)
    publico: models.BooleanField = models.BooleanField(default=False)  # Adicionar este campo

    def __str__(self):
        return f"Relatório {self.id} - {self.projeto.titulo}"


class Entrega(models.Model):
    projeto: models.ForeignKey = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    descricao: models.TextField = models.TextField()
    arquivo: models.FileField = models.FileField(upload_to='entregas/')
    dataEnvio: models.DateField = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Entrega {self.id} - {self.projeto.titulo}"


class Atividade(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('concluida', 'Concluída'),
    ]

    projeto: models.ForeignKey = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    descricao: models.TextField = models.TextField()
    status: models.CharField = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    dataRegistro: models.DateField = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Atividade {self.id} - {self.projeto.titulo}"
