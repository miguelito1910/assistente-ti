-- Script de Criação do Banco e Tabela - Assistente Inteligente de TI

CREATE TABLE IF NOT EXISTS problems (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    category VARCHAR(50) NOT NULL CHECK (
        category IN (
            'Hardware',
            'Software',
            'Rede',
            'Segurança',
            'Sistema Operacional',
            'Banco de Dados',
            'Outros'
        )
    ),
    priority VARCHAR(20) NOT NULL CHECK (
        priority IN ('Baixa', 'Média', 'Alta')
    ),
    summary TEXT NOT NULL,
    initial_suggestion TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Índice para acelerar a listagem dos problemas ordenados por data de criação (mais recentes primeiro)
CREATE INDEX IF NOT EXISTS idx_problems_created_at_desc ON problems (created_at DESC);
