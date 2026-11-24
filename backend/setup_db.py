import psycopg

def setup_database():
    print("Conectando ao PostgreSQL...")
    # 1. Conectar ao banco 'postgres' padrão para criar a base 'assistente_ti'
    with psycopg.connect("postgresql://postgres:postgres@localhost:5432/postgres", autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'assistente_ti'")
            if not cur.fetchone():
                cur.execute("CREATE DATABASE assistente_ti")
                print("-> Banco de dados 'assistente_ti' criado com sucesso!")
            else:
                print("-> Banco de dados 'assistente_ti' já existe.")

    # 2. Conectar ao novo banco 'assistente_ti' e criar as tabelas
    with psycopg.connect("postgresql://postgres:postgres@localhost:5432/assistente_ti", autocommit=True) as conn:
        with open("schema.sql", "r", encoding="utf-8") as f:
            sql_schema = f.read()
        with conn.cursor() as cur:
            cur.execute(sql_schema)
            print("-> Tabela 'problems' e índices criados com sucesso!")

if __name__ == "__main__":
    setup_database()
