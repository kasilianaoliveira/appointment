
# Appointment  API

API para gerenciamento de agendamentos de serviços de informática, permitindo que
clientes realizem agendamentos com base na disponibilidade de administradores
responsáveis pela execução dos serviços.

O projeto foi desenvolvido utilizando **FastAPI**, **PostgreSQL** e **SQLAlchemy**.

## 📌 Visão Geral

A aplicação permite:

- Cadastro e autenticação de usuários (admin e cliente)
- Definição de serviços disponíveis
- Cadastro de disponibilidade de administradores
- Agendamento de serviços por clientes
- Associação de múltiplos serviços a um mesmo agendamento
- Notificações por e-mail (cadastro, agendamento e lembretes)

## 🧱 Arquitetura

O projeto segue uma arquitetura em camadas (Layered Architecture) com separação clara de responsabilidades:

- **Routers**: Endpoints da API, validação de entrada
- **Services**: Lógica de negócio e orquestração
- **Repositories**: Acesso a dados, queries SQLAlchemy
- **Models**: Entidades do banco de dados (ORM)
- **Schemas**: Validação e serialização de dados (Pydantic)
- **Dependencies**: Injeção de dependências do FastAPI
- **Core**: Configurações, segurança, exceções e utilitários

## 🧩 Modelagem de Dados

Principais tabelas:

- users: usuários do sistema (admin e cliente)

- services: catálogo de serviços disponíveis

- appointments: agendamentos realizados

- appointment_services: relação entre agendamentos e serviços

- admin_availability: horários disponíveis dos administradores

## 🔐 Autenticação e Autorização

- Autenticação baseada em JWT

- Login via e-mail e senha

- Controle de acesso baseado em role (admin | user)

- Tokens assinados e com tempo de expiração

## 🚀 Como Rodar o Projeto

- Pré-requisitos

  - Docker e Docker Compose

  - Python 3.11+

- Subindo banco de dados

    ```bash
    docker-compose up -d

    ```

- Criando ambiente virtual

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

- Sicronizando as dependencias

    ```bash
    uv sync
    ```

- Rodando a aplicação

    ```bash
    task run
    ```

- A API estará disponível em: <http://localhost:8000/docs>

## 🗂 Estrutura de Pastas

```text
src/
├── app.py                    # Aplicação FastAPI principal
├── core/                     # Configurações e utilitários centrais
│   ├── db/
│   │   ├── base.py          # Base do SQLAlchemy
│   │   ├── dependencies.py  # Dependências do banco
│   │   └── session.py        # Configuração de sessão
│   ├── exceptions/
│   │   ├── base_exception.py
│   │   ├── error_handlers.py
│   │   └── user_expection.py
│   ├── logging_config.py
│   ├── security.py           # JWT e hash de senhas
│   └── settings.py           # Configurações da aplicação
│
├── dependencies/             # Dependências do FastAPI
│   ├── auth_dependencies.py
│   └── pagination_dependencies.py
│
├── enums/                    # Enumerações
│   ├── user_role.py
│   └── user_date_filter.py
│
├── models/                   # Modelos SQLAlchemy (ORM)
│   ├── user_model.py
│   ├── service_model.py
│   ├── appointment_model.py
│   ├── appointment_service_model.py
│   └── admin_availability_model.py
│
├── repositories/            # Camada de acesso a dados
│   ├── interfaces/
│   │   └── user_interface.py
│   └── user_repository.py
│
├── routers/                 # Rotas/Endpoints da API
│   └── user_router.py
│
├── schemas/                 # Schemas Pydantic (validação)
│   ├── user_schema.py
│   └── token_schema.py
│
└── services/                # Lógica de negócio
    ├── auth_service.py
    └── user_service.py
```

**Fluxo de dados:** `Router → Service → Repository → Model`

## 🧪 Testes
