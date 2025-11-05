from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'propostas', views.PropostaViewSet, basename='propostas')
router.register(r'projetos', views.ProjetoViewSet)
router.register(r'relatorios', views.RelatorioViewSet)
router.register(r'atividades', views.AtividadeViewSet)
router.register(r'entregas', views.EntregaViewSet)

# URLs públicas
router.register(
    r'publico/projetos',
    views.ProjetoPublicoViewSet,
    basename='publico-projetos'
)
router.register(
    r'publico/relatorios',
    views.RelatorioPublicoViewSet,
    basename='publico-relatorios'
)

urlpatterns = [
    path('', include(router.urls)),

    # Autenticação
    path(
        'auth/registro/', views.registro_comunidade,
        name='registro-comunidade'
    ),
    path('auth/login/', views.login_usuario, name='login'),
    path('auth/logout/', views.logout_usuario, name='logout'),
    path('auth/perfil/', views.perfil_usuario, name='perfil'),
]
