from django.core.management.base import BaseCommand
from api.models.profissao import Profissao

class Command(BaseCommand):
    help = "Inicializa o banco com alguns dados pre-definidos."

    def handle(self, *args, **kwargs):
        professions = [
            "Medicina",
            "Odontologia",
            "Fisioterapia",
            "Nutricao",
            "Fonoaudiologia",
            "Enfermagem",
            "Psicologia",
        ]

        for profession in professions:
            Profissao.objects.get_or_create(nome=profession)

        self.stdout.write(self.style.SUCCESS("Tabela Profissao inicializada com sucesso!"))
