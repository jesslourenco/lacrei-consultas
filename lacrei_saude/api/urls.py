from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views.profissional_de_saude_view import ProfissionalDeSaudeView
from api.views.paciente_view import PacienteView
from api.views.consulta_view import ConsultaView

router = DefaultRouter()
router.register(r'profissionais', ProfissionalDeSaudeView, basename="profissional")
router.register(r'pacientes', PacienteView, basename="paciente")
router.register(r'consultas', ConsultaView, basename="consulta")

urlpatterns = [
    path("", include(router.urls)),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),  
    path("docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
