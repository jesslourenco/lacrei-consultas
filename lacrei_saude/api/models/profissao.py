from django.db import models

class Profissao(models.Model):
    nome: str = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.name
