from typing import Optional, List
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from api.repositories.consulta_repo import ConsultaRepo
from api.models.consulta import Consulta

def validate_appt(profissional_id: int, data_hora):
    """ Valida se os dia e hora da consulta sao validos (dentro do horario comercial, segunda a sexta)
        e se o horario desejado ja nao foi agendado.
    """
    if ConsultaRepo.get_by_provider_and_datetime(profissional_id, data_hora):
        raise ValidationError("Horário já está agendado para este profissional.")
        
    if data_hora.hour < 8 or data_hora.hour >= 18:
        raise ValidationError("Consultas devm ser agendadas entre 08:00 e 18:00.")
    
    if data_hora.weekday() in [5, 6]: 
        raise ValidationError("A consulta não pode ser agendada em finais de semana.")

class ConsultaService:
    def list_appts() -> List[Consulta]:
        return ConsultaRepo.get_all()

    def get_appt(pk: int) -> Optional[Consulta]:
        consulta = ConsultaRepo.get_by_id(pk)
        if not consulta:
            raise ValidationError("Consulta não encontrada.")
        return consulta

    def get_upcoming_appts_by_provider(profissional_id: int) -> List[Consulta]:
        return ConsultaRepo.get_upcoming_by_provider(profissional_id)

    def book_appt(paciente_id: int, profissional_id: int, data_hora) -> Consulta:
        validate_appt(profissional_id, data_hora)

        return ConsultaRepo.create(paciente_id, profissional_id, data_hora)

    def update_appt(pk: int, data: dict) -> Consulta:
        appt = ConsultaRepo.get_by_id(pk)
        if not appt:
            raise ObjectDoesNotExist("Consulta nao encontrada.")
        
        validate_appt(appt.profissional_id, data["data_hora"])
        
        return ConsultaRepo.update(appt, data)

    def delete_consulta(pk: int) -> None:
        appt = ConsultaRepo.get_by_id(pk)
        if not appt:
            raise ObjectDoesNotExist("Consulta nao encontrada.")
        ConsultaRepo.delete(appt)
        
