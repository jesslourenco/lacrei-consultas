from django.core.management.base import BaseCommand
from api.models.profissao import Profissao
from api.models.profissional_de_saude import ProfissionalDeSaude
from api.models.paciente import Paciente

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
        
        medicina, _ = Profissao.objects.get_or_create(nome="Medicina")
        provider, created_prof = ProfissionalDeSaude.objects.get_or_create(
            nome_completo="Dr. João Silva",
            profissao=medicina,
            endereco="Rua Exemplo, 123",
            cep="12345-678",
            cidade="São Paulo",
            uf="SP",
            contato="joao.silva@example.com",
            numero_inscricao_profissional="CRM-123456",
        )

        if created_prof:
            self.stdout.write(self.style.SUCCESS("Tabela Profissional inicializada com sucesso!"))
        
        pacient, created_pac = Paciente.objects.get_or_create(
            nome_completo="Maria Oliveira",
            endereco="Av. Saúde, 456",
            cep="12345-678",
            cidade="São Paulo",
            uf="SP",
            contato="maria.oliveira@example.com",
        )

        if created_pac:
            self.stdout.write(self.style.SUCCESS("Tabela Paciente inicializada com sucesso!"))
