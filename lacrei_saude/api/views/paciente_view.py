from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from api.services.paciente_service import PacienteService
from api.serializers.paciente_serializer import PacienteSerializer

@extend_schema_view(
    retrieve=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    update=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)],
        request=PacienteSerializer
    ),
    destroy=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    create=extend_schema(
        request=PacienteSerializer
    )
)

class PacienteView(ViewSet):
    serializer_class = PacienteSerializer
    
    def list(self, request: Request) -> Response:
        pacients = PacienteService.list_pacients()
        serializer = self.serializer_class(pacients, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk: int = None) -> Response:
        try:
            pacient = PacienteService.get_pacient(pk)
            serializer = self.serializer_class(pacient)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pacient = PacienteService.create_pacient(serializer.validated_data)
            return Response(self.serializer_class(pacient).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk: int = None) -> Response:
        try:
            pacient = PacienteService.get_pacient(pk) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=pacient, data=request.data, partial=True) 
        if serializer.is_valid():
            try:
                updated_pacient = PacienteService.update_pacient(pk, serializer.validated_data)
                return Response(self.serializer_class(updated_pacient).data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def destroy(self, request: Request, pk: int = None) -> Response:
        try:
            PacienteService.delete_pacient(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
