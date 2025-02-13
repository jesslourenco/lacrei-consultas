from rest_framework.test import APITestCase
from rest_framework import status
from django.utils.timezone import now, timedelta
from django.utils.dateparse import parse_datetime
from api.models.paciente import Paciente
from api.models.profissional_de_saude import ProfissionalDeSaude
from api.models.consulta import Consulta
from api.models.profissao import Profissao

START_TIME = 8 # inicio horario comercial
END_TIME = 18 # termino horario comercial

def set_valid_date_time(days=1):
    future_date = now() + timedelta(days)
    
    while future_date.weekday() in [5, 6]:  
        future_date += timedelta(days=1)
        
    if future_date.hour < START_TIME:
        future_date = future_date.replace(hour=9, minute=0, second=0)
        
    if future_date.hour >= END_TIME:
        future_date = future_date.replace(hour=15, minute=0, second=0)
        
    return future_date

def set_past_date():
    past_date = now() - timedelta(days=1)
    
    return past_date
    
class ConsultaAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.profissao = Profissao.objects.create(nome="Medicina")
        
        cls.paciente = Paciente.objects.create(
            nome_completo="Maria Oliveira",
            endereco="Av. Saúde, 456",
            cep="98765-432",
            cidade="Rio de Janeiro",
            uf="RJ",
            contato="maria.oliveira@example.com",
        )

        cls.profissional = ProfissionalDeSaude.objects.create(
            nome_completo="Dr. João Silva",
            endereco="Rua Exemplo, 123",
            cep="12345-678",
            cidade="São Paulo",
            uf="SP",
            contato="joao.silva@example.com",
            numero_inscricao_profissional="CRM-123456",
            profissao=cls.profissao, 
        )
        
        cls.profissional2 = ProfissionalDeSaude.objects.create(
        nome_completo="Dra. Ana Souza",
        endereco="Av. Paulista, 987",
        cep="04567-890",
        cidade="Rio de Janeiro",
        uf="RJ",
        contato="ana.souza@example.com",
        numero_inscricao_profissional="CRM-654321",
        profissao=cls.profissao,
        )

    
    def setUp(self):
        self.profissional = self.__class__.profissional
        
        self.consulta = Consulta.objects.create(
            paciente=self.paciente,
            profissional=self.profissional,
            data_hora=set_valid_date_time().isoformat(), 
        )
        
        self.consulta2 = Consulta.objects.create(
            paciente=self.paciente,
            profissional=self.profissional2,
            data_hora=set_valid_date_time(2).isoformat(), 
        )

        self.payload = {
            "paciente": self.paciente.id,
            "profissional": self.profissional.id,
            "data_hora": set_valid_date_time().isoformat(), 
        }
        

    def test_list_appts(self):
        response = self.client.get("/api/consultas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)  
        
    def test_retrieve_appt(self):
        response = self.client.get(f"/api/consultas/{self.consulta.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.consulta.id)
        
    def test_retrieve_upcoming_appt_by_provider(self):
        response = self.client.get(f"/api/consultas/upcoming/{self.profissional.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)  

    def test_create_appt_success(self): 
        response = self.client.post("/api/consultas/", self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["paciente"], self.payload["paciente"])
        self.assertEqual(response.data["profissional"], self.payload["profissional"])

    def test_create_appt_failure_past_date(self):
        self.payload["data_hora"] = set_past_date().isoformat()
        
        response = self.client.post("/api/consultas/", self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A consulta nao pode ser agendada para o passado.", str(response.data["data_hora"][0]))
        
    def test_update_appt(self):
        updated_data = {
            "data_hora": set_valid_date_time().isoformat()
        }
        
        response = self.client.put(f"/api/consultas/{self.consulta.id}/", updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_datetime = parse_datetime(response.data["data_hora"]).isoformat()
        expected_datetime = parse_datetime(updated_data["data_hora"]).isoformat()

        self.assertEqual(response_datetime, expected_datetime)
        
    def test_delete_appt(self):
        response = self.client.delete(f"/api/consultas/{self.consulta.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Consulta.objects.filter(id=self.consulta.id).exists())


