import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipo_usuario', models.CharField(choices=[('comunidade', 'Comunidade Externa'), ('coordenador', 'Coordenador'), ('professor', 'Professor'), ('aluno', 'Aluno'), ('admin', 'Administrador')], default='comunidade', max_length=20)),
                ('telefone', models.CharField(blank=True, max_length=20)),
                ('organizacao', models.CharField(blank=True, max_length=100)),
                ('data_registro', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('objetivos', models.TextField()),
                ('impacto_esperado', models.TextField()),
                ('status', models.CharField(choices=[('em_execucao', 'Em Execução'), ('concluido', 'Concluído'), ('suspenso', 'Suspenso')], default='em_execucao', max_length=20)),
                ('data_inicio', models.DateField()),
                ('data_termino_prevista', models.DateField(blank=True, null=True)),
                ('data_conclusao', models.DateField(blank=True, null=True)),
                ('professor_responsavel', models.ForeignKey(blank=True, limit_choices_to={'tipo_usuario': 'professor'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projetos_como_professor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Entrega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('arquivo', models.FileField(upload_to='entregas/')),
                ('dataEnvio', models.DateField(auto_now_add=True)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('concluida', 'Concluída')], default='pendente', max_length=20)),
                ('dataRegistro', models.DateField(auto_now_add=True)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.projeto')),
            ],
        ),
        migrations.CreateModel(
            name='Proposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descricao', models.TextField()),
                ('problema_resolver', models.TextField()),
                ('publico_alvo', models.TextField()),
                ('relevancia_social', models.TextField()),
                ('status', models.CharField(choices=[('enviada', 'Enviada'), ('em_analise', 'Em Análise'), ('aprovada', 'Aprovada'), ('rejeitada', 'Rejeitada')], default='em_analise', max_length=20)),
                ('data_submissao', models.DateTimeField(auto_now_add=True)),
                ('documentos', models.FileField(blank=True, null=True, upload_to='documentos_propostas/')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propostas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='projeto',
            name='proposta_origem',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='projeto_gerado', to='core.proposta'),
        ),
        migrations.CreateModel(
            name='Relatorio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('conteudo', models.TextField()),
                ('data_relatorio', models.DateField()),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('arquivo', models.FileField(blank=True, null=True, upload_to='relatorios/')),
                ('publico', models.BooleanField(default=False)),
                ('projeto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relatorios', to='core.projeto')),
            ],
        ),
    ]
