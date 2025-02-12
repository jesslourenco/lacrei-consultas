from typing import List
from api.repositories.profissional_de_saude_repo import ProfissionalDeSaudeRepo
from api.models.profissional_de_saude import ProfissionalDeSaude
from django.core.exceptions import ObjectDoesNotExist

class ProfissionalDeSaudeService:
    @staticmethod
    def list_providers() -> List[ProfissionalDeSaude]:
        return list(ProfissionalDeSaudeRepo.get_all())

    @staticmethod
    def get_provider(pk: int) -> ProfissionalDeSaude:
        provider = ProfissionalDeSaudeRepo.get_by_id(pk)
        if not provider:
            raise ObjectDoesNotExist("Profissional nao encontrado.")
        return provider

    @staticmethod
    def create_provider(data: dict) -> ProfissionalDeSaude:
        return ProfissionalDeSaudeRepo.create(data)

    @staticmethod
    def update_provider(pk: int, data: dict) -> ProfissionalDeSaude:
        provider = ProfissionalDeSaudeRepo.get_by_id(pk)
        if not provider:
            raise ObjectDoesNotExist("Profissional nao encontrado.")
        return ProfissionalDeSaudeRepo.update(provider, data)

    @staticmethod
    def delete_provider(pk: int) -> None:
        provider = ProfissionalDeSaudeRepo.get_by_id(pk)
        if not provider:
            raise ObjectDoesNotExist("Profissional nao encontrado.")
        ProfissionalDeSaudeRepo.delete(provider)
