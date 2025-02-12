from rest_framework import serializers
from api.models.profissao import Profissao

class ProfissaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissao
        fields = "__all__"
