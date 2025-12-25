
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

## 🗂 Estrutura de Pastas

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

## 🧪 Testes

app/
├── core/
│   ├── **init**.py
│   ├── db/
    │   ├── **init**.py
│   ├── security.py
│   └── settings.py
│
├── models/
│   ├── **init**.py
│   ├── user_model.py
│   └── user_role.py
│
├── repositories/
│   ├── **init**.py
│   ├── interfaces/
    │   ├── **init**.py
│   │   └── user_interface.py
│   └── user_repository.py
│
├── services/
│   ├── **init**.py
│   ├── auth_service.py
│   └── user_service.py
│
├── schemas/
│   ├── **init**.py
│   ├── user_schema.py
│   └── token_schema.py
│
├── enums/
│   ├── **init**.py
│   ├── user_role.py
│   └── user_date_filter.py
│
├── routes/
│   ├── **init**.py
│   └── user_routes.py
│
└── main.py

order: Model → Schema → Repository → Service → Router.
