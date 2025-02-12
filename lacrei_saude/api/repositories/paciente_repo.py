from typing import Optional 
from django.db.models import QuerySet
from api.models.paciente import Paciente

class PacienteRepo:
    @staticmethod
    def get_all() -> QuerySet[Paciente]:
        return Paciente.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> Optional[Paciente]:
        return Paciente.objects.filter(pk=pk).first()

    @staticmethod
    def create(data: dict) -> Paciente:
        return Paciente.objects.create(**data)

    @staticmethod
    def update(profissional: Paciente, data: dict) -> Paciente:
        for key, value in data.items():
            setattr(profissional, key, value)
        profissional.save()
        return profissional

    @staticmethod
    def delete(profissional: Paciente) -> None:
        profissional.delete()