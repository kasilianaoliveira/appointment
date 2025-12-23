# appointment

app/
├── core/
│   ├── __init__.py
│   ├── db/
    │   ├── __init__.py
│   ├── security.py
│   └── settings.py
│
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   └── user_role.py
│
├── repositories/
│   ├── __init__.py
│   ├── interfaces/
    │   ├── __init__.py
│   │   └── user_interface.py
│   └── user_repository.py
│
├── services/
│   ├── __init__.py
│   ├── auth_service.py
│   └── user_service.py
│
├── schemas/
│   ├── __init__.py
│   ├── user_schema.py
│   └── token_schema.py
│
├── enums/
│   ├── __init__.py
│   ├── user_role.py
│   └── user_date_filter.py
│
├── routes/
│   ├── __init__.py
│   └── user_routes.py
│
└── main.py

order: Model → Schema → Repository → Service → Router.
