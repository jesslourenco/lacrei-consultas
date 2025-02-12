from django.db import models

from .profissao import Profissao
from .utils import email_validator, cep_validator, sanitize_fields

class ProfissionalDeSaude(models.Model):
    nome_completo: str = models.CharField(max_length=255)
    nome_social: str | None = models.CharField(max_length=255, blank=True, null=True)
    profissao: Profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT, related_name="profissional")
    endereco: str = models.TextField()
    cep: str = models.CharField(max_length=9, validators=[cep_validator])
    cidade: str = models.CharField(max_length=100)
    uf: str = models.CharField(max_length=2)
    contato: str = models.CharField(max_length=255, unique=True, validators=[email_validator]) 
    numero_inscricao_profissional: str = models.CharField(max_length=50, unique=True)

    def clean(self) -> None:
        sanitize_fields(self, ["nome_completo", "nome_social", "endereco", "cidade", "uf", "numero_inscricao_profissional"])

    def __str__(self) -> str:
        return f"{self.nome_completo} - {self.profissao.nome} ({self.numero_inscricao_profissional}), contato: {self.contato},"

