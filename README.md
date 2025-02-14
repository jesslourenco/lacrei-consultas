# lacrei-consultas
API Restful que permite o gerenciamento completo de consultas médicas, profissionais de saúde, e pacientes com foco em funcionalidade, segurança e boas práticas.

<a id="readme-top"></a>
<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#sobre-o-projeto">Sobre o Projeto</a>
      <ul>
        <li><a href="#tecnologias"> Tecnologias </a></li>
      </ul>
      <ul>
        <li><a href="#decisões-de-arquitetura-e-design-de-código">Decisões de Arquitetura e Design de Código</a></li>
      </ul>
      <ul>
        <li><a href="#considerações">Considerações</a></li>
      </ul>
    </li>
    <li>
      <a href="#vamos-comecar?">Vamos comecar? </a>
      <ul>
        <li><a href="#pre-requisitos">Pre-requisitos</a></li>
        <li><a href="#como-configurar-o-ambiente-e-rodar-o-projeto">Como Configurar o Ambiente e Rodar o Projeto</a></li>
        <li><a href="#descrição-dos-endpoints"> Descrição dos Endpoints </a></li
        <li><a href="#como-interagir-com-a-api">Como Interagir Com a API</a></li>
        <li><a href="#como-rodar-os-testes-unitários">Como Rodar os Testes Unitários</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Melhorias</a></li>
    <li><a href="#contact">Contato</a></li>
  </ol>
</details>

<!-- SOBRE O PROJETO -->
## Sobre o Projeto
### Tecnologias
Linguagem : <b>Python</b>

Frameworks: <b>Django</b> e <b>Django REST Framework (DRF)</b>

Banco de Dados: <b>PostgeSQL</b>

Ambiente: <b>Docker</b> com <b>Docker-Compose</b>. A aplicação foi completamente containerizada, principalmente para garantir que o código seja executado da mesma forma em qualquer máquina. O Docker Compose foi utilizado para facilitar sua configuração e modo de rodar o projeto.

Gerenciador de pacotes: <b>Poetry</b>. Usado no projeto para simplificar o gerenciamento e instalação de dependências no container.

Testes Unitários: construídos com `APITestCase`, uma classe de teste do DRF que estende a funcionalidade de TestCase do Django, permitindo testar a API por meio da simulação de requisições HTTP. Os testes são isolados, garantindo que cada execução ocorra em um banco de dados temporário, evitando qualquer impacto nos dados reais.

Dependências:
- <b>bleach:</b> biblioteca usada para sanitização de HTML, garantindo a remoção de inputs potencialmente maliciosos, como scripts XSS. Utilizada no projeto para limpar inputs de texto que serão armazenados no banco de dados, garantindo segurança contra ataques de injeção de HTML/JavaScript.
- <b>drf-spectacular:</b> ferramenta para gerar documentação automaticamente no padrão OpenAPI. Usada no projeto para simplificar a manutenção de especificações e facilitar testes manuais.
- <b>email-validator:</b> usado no projeto em conjunto com uma REGEX mais restrita para validar endereços de e-mail, garantindo que os dados inseridos pelos usuários sigam um formato correto e sejam válidos.
- <b>psycopg2-binary:</b> driver usado para conectar o Django ao banco de dados PostgreSQL. A versão "binary" foi escolhida a fim de agilizar a configuração do ambiente no container Docker, pois ela já vem com todas as suas dependências compiladas.

### Decisões de Arquitetura e Design de Código
#### Arquitetura em Camadas
O projeto segue uma arquitetura em camadas, separando claramente as responsabilidades dentro do código. Essa estrutura facilita a compreensão, manutenção/desenvolvimento, testes e evolução do sistema. As camadas principais são:
- Camada de Apresentação (Views/Serializers): Responsável por processar requisições e formatar requests/responses JSON.
- Camada de Serviço (Services): Contém a lógica de negócios central da aplicação.
- Camada de Domínio/Dados (Models): Define as entidades principais com algumas validações gerais de formato de dados.
- Camada de Infraestrutura (Repositories): Gerencia a persistência dos dados com PostgreSQL.

#### Programação Orientada a Objetos (POO)
A escolha de Programação Orientada a Objetos (POO) neste projeto foi feita para garantir um código mais limpo, modular, reutilizável e organizado. Além disso, o paradigma também é utilizado pelo Django e pelo DRF.

#### Uso de Type Hints
O projeto faz uso extensivo de Type Hints para melhorar a legibilidade, manutenção e confiabilidade do código. O suporte a tipagem estática no Python ajuda a detectar erros mais cedo, melhorar a experiência de desenvolvimento e facilitar a colaboração em equipe em projetos reais.

#### Uso do Django ORM
O projeto faz uso do ORM (Object-Relational Mapping) do Django para interagir com o banco de dados, eliminando a necessidade de escrever SQL manualmente. Essa abordagem foi escolhida principalmente para prevenir vulnerabilidades como SQL Injection, uma vez que o ORM do Django sanitiza automaticamente as consultas.

Além disso, o ORM oferece diversas funcionalidades integradas que facilitam o desenvolvimento e a manutenção do banco de dados, como migrações automáticas, gerenciamento de relacionamentos entre tabelas e validação de dados.

#### Considerações
- A maioria das decisões foram guiadas pelo objetivo de facilitar a configuração tanto da aplicação quanto do ambiente. No entanto, algumas dessas escolhas não seguem as melhores práticas para um ambiente de produção. Um exemplo disso é o uso de Docker Compose para a orquestração do ambiente.
- O projeto utiliza um usuário padrão do PostgreSQL, com credenciais definidas diretamente no arquivo Docker Compose. Além disso, diversas variáveis de ambiente (como PORT) estão expostas no código. Em projetos reais, isso representa uma séria vulnerabilidade de segurança, pois credenciais e configurações sensíveis não devem ser armazenadas nem expostas no GitHub. O ideal seria utilizar arquivos .env e um gerenciador de segredos adequado.
- O gerenciamento dos dados de Profissão é restrito a usuários administradores, e por isso não há uma API exposta para essa entidade. Para simplificar o uso do projeto, essa tabela já vem pré-inicializada e não pode ser modificada. O ideal seria expor esse endpoint apenas para usuários autenticados e autorizados, garantindo o controle de acesso adequado.
- Devido ao tempo limitado do desafio, apenas um dos endpoints conta com testes unitários básicos. No entanto, o ideal seria garantir um test coverage de pelo menos 80%, abrangendo testes unitários e de integração para validar a API de forma mais robusta.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- INSTRUCOES -->
## Pre-requisitos
Antes de começar, verifique se você atende aos seguintes requisitos:
- Ter Docker Desktop e Docker Compose instalados em sua máquina.

Se ainda não os tiver instalados, consulte a [documentação oficial](https://docs.docker.com/get-started/) do Docker para obter as instruções de instalação.

## Como Configurar o Ambiente e Rodar o Projeto
Siga os passos abaixo para configurar e executar o projeto em sua máquina:
1. Clone este repositório: `git clone git@github.com:jesslourenco/lacrei-consultas.git`
2. Acesse o diretório raiz do projeto: `cd lacrei-consultas/lacrei_saude`
3. Certifique-se de que o Docker Desktop está em execução em sua máquina.
4. Construa o container: `docker-compose build`
5. Inicie o container `docker-compose up -d`
6. Caso queira parar a execução: `docker-compose down`

## Descrição dos Endpoints
#### Profissionais
Gerencia profissionais de saúde
- `GET /api/profissionais/` → Retorna a lista de todos os profissionais de saúde cadastrados.
- `GET /api/profissionais/{id}` → Retorna os detalhes de um profissional específico com base no ID.
- `POST /api/profissionais/` → Cria um novo profissional de saúde.
- `PUT /api/profissionais/{id}` → Atualiza os dados de um profissional existente com base no ID.
- `DELETE /api/profissionais/{id}` → Remove um profissional do sistema com base no ID.

#### Pacientes 
Gerencia pacientes
- `GET /api/pacientes/` → Retorna a lista de todos os pacientes cadastrados.
- `GET /api/pacientes/{id}` → Retorna os detalhes de um paciente específico com base no ID
- `POST /api/pacientes/` → Cria um novo paciente no sistema.
- `PUT /api/pacientes/{id}` → Atualiza os dados de um paciente existente com base no ID.
- `DELETE /api/pacientes/{id}` → Remove um paciente do sistema com base no ID.

#### Consultas 
Genrencia o agendamento de consultas entre profissional de saude e paciente
- `GET /api/consultas/` → Retorna a lista de todas as consultas agendadas.
- `GET /api/consultas/upcoming/{profissional_id}` → Retorna as próximas consultas de um determinado profissional com base no ID.
- `GET /api/consultas/{id}` Retorna os detalhes de uma consulta específica com base no ID.
- `POST /api/consultas/` → Cria um novo agendamento de consulta entre um paciente e um profissional de saúde.
- `PUT /api/consultas/{id}` → Atualiza as informações de um agendamento de consulta existente.
- `DELETE /api/consultas/{id}` → Cancela e remove um agendamento de consulta do sistema.

## Como Interagir Com a API
Após iniciar o projeto, a aplicação estará disponível nos seguintes endereços:
- `http://localhost:8000`
- `http://0.0.0.0:8000/`

O projeto está configurado para ser inicializado com alguns dados pré-cadastrados de profissões, profissionais de saúde e pacientes. 😊
As profissões cadastradas correspondem às listadas no site oficial da Lacrei Saúde e possuem IDs entre 1 e 7. 
Caso queira mais detalhes sobre esses dados iniciais, você pode consultar o arquivoo `init_db.py` em `api/management/commands`

Você pode testar e interagir com os endpoints de três formas:
1. Via Interface Gráfica (Swagger) – Recomendado
  - Acesse a documentação interativa no navegador `http://localhost:8000/api/docs`
  - Aqui você pode visualizar e testar os endpoints diretamente pela UI.
2. Via Plataforma para APIs (Postman, Insomnia, etc.)
  - Use ferramentas como Postman ou Insomnia para testar requisições.
  - Basta criar uma nova requisição GET, POST, PUT ou DELETE e apontar para os endpoints da API.
3. Via Linha de Comando (cURL)
  - Caso prefira usar o terminal, você pode usar o cURL para fazer requisições.
  - Ele já vem instalado por padrão no macOS, Linux e Windows 10/11. Verifique com o comando `curl --version`.
  - Exemplo de uma requisição GET: `curl -X GET http://localhost:8000/api/profissionais`

## Como Rodar os Testes Unitários
Siga os passos abaixo para executar os testes unitários do projeto:
- Certifique-se de estar no diretório raiz do projeto `lacrei_saude`
- Inicie o container caso esteja parado `docker-compose up -d`
- Execute os testes unitários dentro do container: `docker exec -it lacrei-saude-api python manage.py test tests/`
- O resultado será exibido no terminal.



