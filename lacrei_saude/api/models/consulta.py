from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from api.models.paciente import Paciente
from api.models.profissional_de_saude import ProfissionalDeSaude

def validate_future_date(value):
    """Valida se o dia e horario da consulta esta no futuro."""
    if value < timezone.now():
        raise ValidationError("A consulta nao pode ser agendada para o passado.")
    
def validate_working_hours(value):
    """
        Valida se o horario da consulta esta dentro do horario comercial (entre 08:00 e 18:00)
        e se o dia da consulta eh dia de semana.
    """
    if value.hour < 8 or value.hour > 18:
        raise ValidationError("A consulta deve ser entre 08:00 e 18:00.")
    
    if value.weekday() in [5, 6]:  # 5 = Saturday, 6 = Sunday
        raise ValidationError("A consulta não pode ser agendada para fins de semana.")

class Consulta(models.Model):
    paciente: Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    profissional: ProfissionalDeSaude = models.ForeignKey(ProfissionalDeSaude, on_delete=models.CASCADE, related_name="consultas")
    data_hora = models.DateTimeField(validators=[validate_future_date, validate_working_hours])
    
    class Meta:
        unique_together = ("profissional", "data_hora")

    def __str__(self):
        return f"Consulta: {self.paciente.nome_completo} com {self.profissional.nome_completo} em {self.data_hora}"