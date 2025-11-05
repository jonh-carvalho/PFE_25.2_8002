from django.contrib.auth import login, logout
from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .models import Atividade, Entrega, Projeto, Proposta, Relatorio, Usuario
from .serializers import (AtividadeSerializer, EntregaSerializer,
                          LoginSerializer, ProjetoListSerializer,
                          ProjetoSerializer, PropostaCreateSerializer,
                          PropostaListSerializer, PropostaSerializer,
                          RegistroComunidadeSerializer,
                          RelatorioPublicoSerializer, RelatorioSerializer,
                          UsuarioSerializer)


# Views de Autenticação
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registro_comunidade(request):
    serializer = RegistroComunidadeSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UsuarioSerializer(user).data,
            'token': token.key,
            'message': 'Usuário criado com sucesso'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_usuario(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UsuarioSerializer(user).data,
            'token': token.key,
            'message': 'Login realizado com sucesso'
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout_usuario(request):
    Token.objects.filter(user=request.user).delete()
    logout(request)
    return Response({'message': 'Logout realizado com sucesso'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def perfil_usuario(request):
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)


# Permissões Customizadas
class IsComunidadeExterna(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tipo_usuario == 'comunidade')


class IsCoordenador(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and
                request.user.tipo_usuario == 'coordenador')


class IsComunidadeOrCoordenador(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.tipo_usuario == 'comunidade' or
            request.user.tipo_usuario == 'coordenador'
        )


# Atualizar PropostaViewSet com autenticação
class PropostaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsComunidadeOrCoordenador]

    def get_queryset(self):
        user = self.request.user
        if user.tipo_usuario == 'coordenador':
            return Proposta.objects.all().order_by('-data_submissao')
        else:  # comunidade externa
            return Proposta.objects.filter(
                usuario=user
            ).order_by('-data_submissao')

    def get_serializer_class(self):
        if self.action == 'list':
            return PropostaListSerializer
        elif self.action == 'create':
            return PropostaCreateSerializer
        return PropostaSerializer

    def perform_create(self, serializer):
        # O usuário já é associado automaticamente pelo
        # PropostaCreateSerializer
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsCoordenador])
    def aprovar(self, request, pk=None):
        proposta = self.get_object()
        proposta.status = 'aprovada'
        proposta.save()

        # Criar projeto automaticamente a partir da proposta aprovada
        projeto = Projeto.objects.create(
            titulo=proposta.titulo,
            descricao=proposta.descricao,
            objetivos=proposta.problema_resolver,
            impacto_esperado=proposta.relevancia_social,
            proposta_origem=proposta,
            data_inicio=timezone.now().date()
        )

        return Response({
            'message': 'Proposta aprovada e projeto criado com sucesso',
            'projeto_id': projeto.id
        })

    @action(detail=True, methods=['post'], permission_classes=[IsCoordenador])
    def rejeitar(self, request, pk=None):
        proposta = self.get_object()
        proposta.status = 'rejeitada'
        proposta.save()
        return Response({'message': 'Proposta rejeitada'})


# Atualizar ProjetoViewSet
class ProjetoViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Projeto.objects.all().order_by('-data_inicio')

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjetoListSerializer
        return ProjetoSerializer

    @action(detail=True, methods=['get'])
    def relatorios(self, request, pk=None):
        projeto = self.get_object()
        relatorios = projeto.relatorios.all()
        serializer = RelatorioSerializer(relatorios, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def atividades(self, request, pk=None):
        projeto = self.get_object()
        atividades = projeto.atividades.all()
        serializer = AtividadeSerializer(atividades, many=True)
        return Response(serializer.data)


# Views públicas (sem autenticação necessária)
class ProjetoPublicoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Projeto.objects.filter(
        status='em_execucao'
    ).order_by('-data_inicio')
    serializer_class = ProjetoListSerializer

    @action(detail=True, methods=['get'])
    def detalhes(self, request, pk=None):
        projeto = self.get_object()
        serializer = ProjetoSerializer(projeto)
        return Response(serializer.data)


class RelatorioPublicoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Relatorio.objects.filter(
        publico=True
    ).order_by('-data_relatorio')
    serializer_class = RelatorioPublicoSerializer


class RelatorioViewSet(viewsets.ModelViewSet):
    queryset = Relatorio.objects.all()
    serializer_class = RelatorioSerializer


class EntregaViewSet(viewsets.ModelViewSet):
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer


class AtividadeViewSet(viewsets.ModelViewSet):
    queryset = Atividade.objects.all()
    serializer_class = AtividadeSerializer
