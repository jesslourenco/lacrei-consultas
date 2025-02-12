from django.contrib import admin
from api.models.profissao import Profissao

@admin.register(Profissao)
class ProfissaoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome")      
    search_fields = ["nome"]  
