# Entity Relationship Diagram

```mermaid
erDiagram
    Users {
        int id PK
        string name
        string email
        string phone
        string address
        datetime created_at
    }

    Admins {
        int id PK
        string username
        string password
        string email
        string role
        datetime created_at
    }

    Products {
        int id PK
        string sku
        string name
        string description
        decimal price
        int quantity
        int min_quantity
        int category_id FK
    }

    Categories {
        int id PK
        string name
        string description
    }

    Stock_Movements {
        int id PK
        int product_id FK
        int quantity
        string movement_type
        datetime date
        string note
        int admin_id FK
    }

    Sales {
        int id PK
        int user_id FK
        int admin_id FK
        datetime date
        decimal total
    }

    Sale_Items {
        int id PK
        int sale_id FK
        int product_id FK
        int quantity
        decimal price
    }

    Products ||--o{ Stock_Movements : "has"
    Categories ||--o{ Products : "contains"
    Users ||--o{ Sales : "makes"
    Admins ||--o{ Sales : "processes"
    Admins ||--o{ Stock_Movements : "records"
    Sales ||--o{ Sale_Items : "contains"
    Products ||--o{ Sale_Items : "included_in"
