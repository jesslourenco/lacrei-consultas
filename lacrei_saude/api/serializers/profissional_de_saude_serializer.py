from rest_framework import serializers
from api.models.profissional_de_saude import ProfissionalDeSaude
from api.models.profissao import Profissao
from api.serializers.profissao_serializer import ProfissaoSerializer

class ProfissionalDeSaudeSerializer(serializers.ModelSerializer):
    profissao = ProfissaoSerializer(read_only=True)
    
    profissao_id = serializers.PrimaryKeyRelatedField(
        queryset=Profissao.objects.all(),
        source="profissao",
        write_only=True
    )

    class Meta:
        model = ProfissionalDeSaude
        fields = [
            "id", 
            "nome_completo", 
            "nome_social", 
            "profissao",     
            "profissao_id",  
            "endereco", 
            "cep", 
            "cidade", 
            "uf", 
            "contato", 
            "numero_inscricao_profissional"
        ]
