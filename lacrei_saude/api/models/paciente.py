from django.db import models

from .utils import email_validator, cep_validator, sanitize_fields

class Paciente(models.Model):
    nome_completo: str = models.CharField(max_length=255)
    nome_social: str | None = models.CharField(max_length=255, blank=True, null=True)
    endereco: str = models.TextField()
    cep: str = models.CharField(max_length=9, validators=[cep_validator])
    cidade: str = models.CharField(max_length=100)
    uf: str = models.CharField(max_length=2)
    contato: str = models.CharField(max_length=255, unique=True, validators=[email_validator]) 

    def clean(self) -> None:
        sanitize_fields(self, ["nome_completo", "nome_social", "endereco", "cidade", "uf"])

    def __str__(self) -> str:
        return f"{self.nome_completo}, contato: {self.contato}"