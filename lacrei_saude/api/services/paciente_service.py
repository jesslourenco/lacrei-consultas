from typing import List
from api.repositories.paciente_repo import PacienteRepo
from api.models.paciente import Paciente
from django.core.exceptions import ObjectDoesNotExist

class PacienteService:
    @staticmethod
    def list_pacients() -> List[Paciente]:
        return list(PacienteRepo.get_all())

    @staticmethod
    def get_pacient(pk: int) -> Paciente:
        pacient = PacienteRepo.get_by_id(pk)
        if not pacient:
            raise ObjectDoesNotExist("Profissional nao encontrado.")
        return pacient

    @staticmethod
    def create_pacient(data: dict) -> Paciente:
        return PacienteRepo.create(data)

    @staticmethod
    def update_pacient(pk: int, data: dict) -> Paciente:
        pacient = PacienteRepo.get_by_id(pk)
        if not pacient:
            raise ObjectDoesNotExist("Profissional nao encontrado.")
        return PacienteRepo.update(pacient, data)

    @staticmethod
    def delete_pacient(pk: int) -> None:
        pacient = PacienteRepo.get_by_id(pk)
        if not pacient:
            raise ObjectDoesNotExist("Paciente nao encontrado.")
        PacienteRepo.delete(pacient)
