from django.db import models
from django.core.exceptions import ValidationError
from email_validator import validate_email, EmailNotValidError
from .profissao import Profissao
import bleach
import re

REGEX_CEP = re.compile(r"^\d{5}-\d{3}$")  # formato XXXXX-XXX

class ProfissionalDeSaude(models.Model):
    nome_completo: str = models.CharField(max_length=255)
    nome_social: str | None = models.CharField(max_length=255, blank=True, null=True)
    profissao: Profissao = models.ForeignKey(Profissao, on_delete=models.PROTECT, related_name="profissional")
    endereco: str = models.TextField()
    cep: str = models.CharField(max_length=9)
    cidade: str = models.CharField(max_length=100)
    uf: str = models.CharField(max_length=2)
    contato: str = models.CharField(max_length=255) 
    numero_inscricao_profissional: str = models.CharField(max_length=50, unique=True)

    def clean(self) -> None:
        """Valida inputs e sanitiza campos vulneraveis."""
        try:
            validate_email(self.contato, check_deliverability=False)
        except EmailNotValidError:
            raise ValidationError("Formato de email invalido.")

        if not REGEX_CEP.match(self.cep):
            raise ValidationError("Formato de CEP invalido. Use XXXXX-XXX.")

        self.nome_completo = bleach.clean(self.nome_completo, tags=[], strip=True)
        self.endereco = bleach.clean(self.endereco, tags=[], strip=True)
        self.cidade = bleach.clean(self.cidade, tags=[], strip=True)
        self.uf = bleach.clean(self.uf, tags=[], strip=True)
        self.numero_inscricao_profissional = bleach.clean(self.numero_inscricao_profissional, tags=[], strip=True)


        if self.nome_social:
            self.nome_social = bleach.clean(self.nome_social, tags=[], strip=True)

    def __str__(self) -> str:
        return f"{self.nome_completo} - {self.profissao.nome} ({self.numero_inscricao_profissional}), contato: {self.contato},"

