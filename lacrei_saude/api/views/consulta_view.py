from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from django.core.exceptions import ValidationError

from api.serializers.consulta_serializer import ConsultaSerializer
from api.services.consulta_service import ConsultaService
from api.models.consulta import Consulta


@extend_schema_view(
    retrieve=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    update=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)],
        request=ConsultaSerializer
    ),
    destroy=extend_schema(
        parameters=[OpenApiParameter(name="id", required=True, type=int, location=OpenApiParameter.PATH)]
    ),
    create=extend_schema(
        request=ConsultaSerializer
    )
)

class ConsultaView(ViewSet):
    serializer_class = ConsultaSerializer
    
    def list(self, request: Request) -> Response:
        appts = ConsultaService.list_appts()
        serializer = self.serializer_class(appts, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, pk=None) -> Response:
        try:
            appt = ConsultaService.get_app(pk)
            serializer = self.serializer_class(appt)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=False, methods=["get"], url_path="upcoming/(?P<profissional_id>\\d+)")
    def retrieve_upcoming_by_provider(self, request: Request, profissional_id: int) -> Response:
        appts = ConsultaService.get_upcoming_appts_by_provider(profissional_id)
        serializer = self.serializer_class(appts, many=True)                                                   
        return Response(serializer.data)

    def create(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            appt = ConsultaService.book_appt(
                paciente_id=serializer.validated_data["paciente"].id,  
                profissional_id=serializer.validated_data["profissional"].id,
                data_hora=serializer.validated_data["data_hora"]
            )
            return Response(self.serializer_class(appt).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request: Request, pk=None) -> Response:
        try:
            appt = ConsultaService.get_appt(pk) 
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=appt, data=request.data, partial=True) 
        if serializer.is_valid():
            try:
                updated_appt = ConsultaService.update_appt(pk, serializer.validated_data)
                return Response(self.serializer_class(updated_appt).data)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    def destroy(self, request: Request, pk=None) -> Response:
        try:
            ConsultaService.delete_consulta(pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)