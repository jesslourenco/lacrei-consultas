from typing import Optional 
from django.db.models import QuerySet
from api.models.profissional_de_saude import ProfissionalDeSaude

class ProfissionalDeSaudeRepo:
    @staticmethod
    def get_all() -> QuerySet[ProfissionalDeSaude]:
        return ProfissionalDeSaude.objects.all()

    @staticmethod
    def get_by_id(pk: int) -> Optional[ProfissionalDeSaude]:
        return ProfissionalDeSaude.objects.filter(pk=pk).first()

    @staticmethod
    def create(data: dict) -> ProfissionalDeSaude:
        return ProfissionalDeSaude.objects.create(**data)

    @staticmethod
    def update(profissional: ProfissionalDeSaude, data: dict) -> ProfissionalDeSaude:
        for key, value in data.items():
            setattr(profissional, key, value)
        profissional.save()
        return profissional

    @staticmethod
    def delete(profissional: ProfissionalDeSaude) -> None:
        profissional.delete()
