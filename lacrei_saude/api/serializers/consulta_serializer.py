from rest_framework import serializers
from api.models.consulta import Consulta

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consulta
        fields = ["id", "paciente", "profissional", "data_hora"]