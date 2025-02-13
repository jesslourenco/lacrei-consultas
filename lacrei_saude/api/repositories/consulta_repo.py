from api.models.consulta import Consulta
from django.db.models import QuerySet
from django.utils.timezone import now
from typing import Optional

from api.models.paciente import Paciente
from api.models.profissional_de_saude import ProfissionalDeSaude

class ConsultaRepo:
    @staticmethod
    def get_all() -> QuerySet[Consulta]:
        return Consulta.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> Optional[Consulta]:
        return Consulta.objects.filter(pk=pk).first()

    @staticmethod
    def get_by_provider_and_datetime(profissional_id: int, data_hora) -> bool:
        return Consulta.objects.filter(profissional_id=profissional_id, data_hora=data_hora).exists()

    @staticmethod
    def get_upcoming_by_provider(profissional_id: int) -> QuerySet[Consulta]:
        return Consulta.objects.filter(profissional_id=profissional_id, data_hora__gte=now())

    @staticmethod
    def create(paciente_id: int, profissional_id: int, data_hora) -> Consulta:
        consulta = Consulta.objects.create(
            paciente_id=paciente_id,
            profissional_id=profissional_id,
            data_hora=data_hora
        )
        return consulta
    
    @staticmethod
    def update(consulta: Consulta, data: dict) -> Consulta:
        for key, value in data.items():
            setattr(consulta, key, value)
        consulta.save()
        return consulta
    
    @staticmethod
    def delete(consulta: Consulta) -> None:
        consulta.delete()
       
