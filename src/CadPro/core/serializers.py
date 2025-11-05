from django.contrib.auth import authenticate
from rest_framework import serializers  # type: ignore

from .models import Atividade, Entrega, Projeto, Proposta, Relatorio, Usuario


# Serializer para registro de usuários da comunidade externa
class RegistroComunidadeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'telefone', 'organizacao', 'password', 'password_confirm'
        ]

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "As senhas não coincidem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = Usuario.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            telefone=validated_data.get('telefone', ''),
            organizacao=validated_data.get('organizacao', ''),
            password=validated_data['password'],
            tipo_usuario='comunidade'

        )
        return user


# Serializer para login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Credenciais inválidas.')
        return attrs


# Serializer para usuário
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'tipo_usuario', 'telefone', 'organizacao'
        ]


class PropostaSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(
        source='usuario.get_full_name',
        read_only=True
    )
    usuario_email = serializers.CharField(
        source='usuario.email',
        read_only=True
    )
    usuario_organizacao = serializers.CharField(
        source='usuario.organizacao',
        read_only=True
    )

    class Meta:
        model = Proposta
        fields = '__all__'
        read_only_fields = ('data_submissao', 'status', 'usuario')


class PropostaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta
        fields = [
            'titulo', 'descricao', 'problema_resolver', 'publico_alvo',
            'relevancia_social', 'documentos'
        ]

    def create(self, validated_data):
        # Associa automaticamente o usuário logado à proposta
        user = self.context['request'].user
        proposta = Proposta.objects.create(usuario=user, **validated_data)
        return proposta


# Atualizar outros serializers conforme necessário...
class ProjetoSerializer(serializers.ModelSerializer):
    professor_nome = serializers.CharField(
        source='professor_responsavel.get_full_name',
        read_only=True
    )

    class Meta:
        model = Projeto
        fields = '__all__'


# Serializers para listagem mantêm os mesmos
class PropostaListSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(
        source='usuario.get_full_name',
        read_only=True
    )

    class Meta:
        model = Proposta
        fields = ['id', 'titulo', 'status', 'data_submissao', 'usuario_nome']


class ProjetoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = [
            'id', 'titulo', 'status', 'data_inicio', 'professor_responsavel'
        ]


class RelatorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relatorio
        fields = '__all__'


class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = '__all__'


class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = '__all__'


# Serializer para Relatorio Público
class RelatorioPublicoSerializer(serializers.ModelSerializer):
    projeto_titulo = serializers.CharField(
        source='projeto.titulo', read_only=True
    )
    projeto_id = serializers.IntegerField(
        source='projeto.id', read_only=True
    )

    class Meta:
        model = Relatorio
        fields = [
            'id', 'titulo', 'conteudo', 'data_relatorio',
            'projeto_titulo', 'projeto_id'
        ]
        read_only_fields = fields
