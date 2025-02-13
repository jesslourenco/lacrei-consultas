from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from api.models.paciente import Paciente
from api.models.profissional_de_saude import ProfissionalDeSaude

def validate_future_date(value):
    """Valida se o dia e horario da consulta esta no futuro."""
    if value < timezone.now():
        raise ValidationError("A consulta nao pode ser agendada para o passado.")

class Consulta(models.Model):
    paciente: Paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    profissional: ProfissionalDeSaude = models.ForeignKey(ProfissionalDeSaude, on_delete=models.CASCADE, related_name="consultas")
    data_hora = models.DateTimeField(validators=[validate_future_date])
    
    class Meta:
        unique_together = ("profissional", "data_hora")

    def __str__(self):
        return f"Consulta: {self.paciente.nome_completo} com {self.profissional.nome_completo} em {self.data_hora}"