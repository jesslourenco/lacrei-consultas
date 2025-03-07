from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from api.services.profissional_de_saude_service import ProfissionalDeSaudeService
from api.serializers.profissional_de_saude_serializer import ProfissionalDeSaudeSerializer

@extend_schema_view(
    retrieve=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    update=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)],
        request=ProfissionalDeSaudeSerializer
    ),
    destroy=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    create=extend_schema(
        request=ProfissionalDeSaudeSerializer
    ),

)

class ProfissionalDeSaudeView(ViewSet):
    serializer_class = ProfissionalDeSaudeSerializer
    
    def list(self, request: Request) -> Response:
        providers = ProfissionalDeSaudeService.list_providers()
        serializer = self.serializer_class(providers, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            provider = ProfissionalDeSaudeService.get_provider(pk)
            serializer = self.serializer_class(provider)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            provider = ProfissionalDeSaudeService.create_provider(serializer.validated_data)
            return Response(self.serializer_class(provider).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk: int = None) -> Response:
        try:
            provider = ProfissionalDeSaudeService.get_provider(pk) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=provider, data=request.data, partial=True) 
        if serializer.is_valid():
            try:
                updated_provider = ProfissionalDeSaudeService.update_provider(pk, serializer.validated_data)
                return Response(self.serializer_class(updated_provider).data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    def destroy(self, request: Request, pk: int = None) -> Response:
        try:
            ProfissionalDeSaudeService.delete_provider(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
