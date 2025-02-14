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
      <a href="#getting-started">Vamos comecar? </a>
      <ul>
        <li><a href="#prerequisites">Pre-requisitos</a></li>
        <li><a href="#run-project">Como Rodar o Projeto</a></li>
        <li><a href="#endpoints">Descricao dos Endpoints </a></li
        <li><a href="#usage">Como Interagir Com a API</a></li>
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

Dependências:
- <b>bleach:</b> biblioteca usada para sanitização de HTML, garantindo a remoção de inputs potencialmente maliciosos, como scripts XSS. Utilizada no projeto para limpar inputs de texto que serão armazenados no banco de dados, garantindo segurança contra ataques de injeção de HTML/JavaScript.
- <b>drf-spectacular:</b> ferramenta para gerar documentação automaticamente no padrão OpenAPI. Usada no projeto para simplificar a manutenção de especificações e facilitar testes manuais.
- <b>email-validator:</b> usado no projeto em conjunto com uma REGEX mais restrita para validar endereços de e-mail, garantindo que os dados inseridos pelos usuários sigam um formato correto e sejam válidos.
- <b>psycopg2-binary:</b> driver usado para conectar o Django ao banco de dados PostgreSQL. A versão "binary" foi escolhida a fim de agilizar a configuração do ambiente no container Docker, pois ela já vem com todas as suas dependências compiladas.

### Decisões de Arquitetura e Design de Código
##### Arquitetura em Camadas
O projeto segue uma arquitetura em camadas, separando claramente as responsabilidades dentro do código. Essa estrutura facilita a compreensão, manutenção/desenvolvimento, testes e evolução do sistema. As camadas principais são:
- Camada de Apresentação (Views/Serializers): Responsável por processar requisições e formatar requests/responses JSON.
- Camada de Serviço (Services): Contém a lógica de negócios central da aplicação.
- Camada de Domínio/Dados (Models): Define as entidades principais com algumas validações gerais de formato de dados.
- Camada de Infraestrutura (Repositories): Gerencia a persistência dos dados com PostgreSQL.

##### Programação Orientada a Objetos (POO)
A escolha de Programação Orientada a Objetos (POO) neste projeto foi feita para garantir um código mais limpo, modular, reutilizável e organizado. Além disso, o paradigma também é utilizado pelo Django e pelo DRF.

##### Uso de Type Hints
O projeto faz uso extensivo de Type Hints para melhorar a legibilidade, manutenção e confiabilidade do código. O suporte a tipagem estática no Python ajuda a detectar erros mais cedo, melhorar a experiência de desenvolvimento e facilitar a colaboração em equipe em projetos reais.

##### Considerações
- A maioria das decisões foram guiadas pelo objetivo de facilitar a configuração tanto da aplicação quanto do ambiente. No entanto, algumas dessas escolhas não seguem as melhores práticas para um ambiente de produção. Um exemplo disso é o uso de Docker Compose para a orquestração do ambiente.
- O projeto utiliza um usuário padrão do PostgreSQL, com credenciais definidas diretamente no arquivo Docker Compose. Além disso, diversas variáveis de ambiente (como PORT) estão expostas no código. Em projetos reais, isso representa uma séria vulnerabilidade de segurança, pois credenciais e configurações sensíveis não devem ser armazenadas nem expostas no GitHub. O ideal seria utilizar arquivos .env e um gerenciador de segredos adequado.
- O gerenciamento dos dados de Profissão é restrito a usuários administradores, e por isso não há uma API exposta para essa entidade. Para simplificar o uso do projeto, essa tabela já vem pré-inicializada e não pode ser modificada. O ideal seria expor esse endpoint apenas para usuários autenticados e autorizados, garantindo o controle de acesso adequado.
- Devido ao tempo limitado do desafio, apenas um dos endpoints conta com testes unitários básicos. No entanto, o ideal seria garantir um test coverage de pelo menos 80%, abrangendo testes unitários e de integração para validar a API de forma mais robusta.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

