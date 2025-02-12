from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from api.services.profissional_de_saude_service import ProfissionalDeSaudeService
from api.serializers.profissional_de_saude_serializer import ProfissionalDeSaudeSerializer
from rest_framework.request import Request
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


class ProfissionalDeSaudeView(ViewSet):
    def list(self, request: Request) -> Response:
        providers = ProfissionalDeSaudeService.list_providers()
        serializer = ProfissionalDeSaudeSerializer(providers, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            provider = ProfissionalDeSaudeService.get_provider(pk)
            serializer = ProfissionalDeSaudeSerializer(provider)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    
    @extend_schema(
        request=ProfissionalDeSaudeSerializer, 
    )
    def create(self, request: Request) -> Response:
        serializer = ProfissionalDeSaudeSerializer(data=request.data)
        if serializer.is_valid():
            provider = ProfissionalDeSaudeService.create_provider(serializer.validated_data)
            return Response(ProfissionalDeSaudeSerializer(provider).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=ProfissionalDeSaudeSerializer, 
    )
    def update(self, request: Request, pk: int = None) -> Response:
        try:
            provider = ProfissionalDeSaudeService.update_provider(pk, request.data)
            return Response(ProfissionalDeSaudeService(provider).data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request: Request, pk: int = None) -> Response:
        try:
            ProfissionalDeSaudeService.delete_provider(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
