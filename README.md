# 🛠️ Assistente Inteligente de TI

Aplicação web completa desenvolvida para automatizar a identificação, classificação, priorização e sugestão inicial de soluções para problemas técnicos de TI relatados por usuários em linguagem natural.

O sistema recebe a descrição do incidente (ex: *"Meu computador está conectado ao Wi-Fi, mas não consigo acessar nenhum site"*), consulta o modelo de inteligência artificial **Google Gemini** forçando saída estruturada em JSON, valida os dados em múltiplas camadas e persiste todo o histórico em banco de dados relacional **PostgreSQL**, oferecendo uma interface reativa em **React + TypeScript**.

---

## 📸 Demonstração do Fluxo

```
[ Usuário relata problema no Frontend ]
                 │
                 ▼
[ POST /problems (FastAPI valida tamanho e formato com Pydantic) ]
                 │
                 ▼
[ Chamada ao Google Gemini SDK (google-genai) com Structured Output ]
                 │
                 ▼
[ Validação estrita da resposta da IA com Pydantic (Enum Category & Priority) ]
                 │
                 ▼
[ INSERT seguro no PostgreSQL (consultas parametrizadas com psycopg3) ]
                 │
                 ▼
[ Resposta retornada ao Frontend com status 201 Created e exibição em tempo real ]
```

---

## 🧰 Tecnologias Utilizadas

### **Backend**
- **Python 3.11+**
- **FastAPI**: Framework web moderno, assíncrono e de alta performance.
- **Google GenAI SDK (`google-genai`)**: Integração oficial com modelos Gemini com saída estruturada (*Structured Outputs*).
- **Pydantic & Pydantic-Settings**: Validação robusta de dados em tempo de execução e gestão tipada de variáveis de ambiente.
- **Psycopg 3 (`psycopg`, `psycopg_pool`)**: Driver moderno para PostgreSQL com suporte a pool de conexões thread-safe.
- **Pytest**: Suíte de testes automatizados com cobertura de schemas, rotas e tratamento de erros através de mocks.

### **Banco de Dados**
- **PostgreSQL 18**
- Modelagem relacional com `CHECK constraints` para categorias e prioridades, índice para consultas ordenadas por data e timestamps com fuso horário.

### **Frontend**
- **React 19**
- **TypeScript**
- **Vite**
- **CSS3 Vanilla**: Layout responsivo com tema Dark moderno, sem dependências externas de UI.

---

## 📋 Categorias e Prioridades

### Categorias Suportadas:
- `Hardware`
- `Software`
- `Rede`
- `Segurança`
- `Sistema Operacional`
- `Banco de Dados`
- `Outros`

### Níveis de Prioridade:
- **Baixa**: Incidentes que não comprometem significativamente as atividades.
- **Média**: Problemas que prejudicam parcialmente as atividades cotidianas.
- **Alta**: Incidentes críticos que afetam atividades essenciais ou múltiplos usuários.

---

## 📂 Estrutura do Projeto

```text
assistente-ti/
├── backend/
│   ├── app/
│   │   ├── main.py              # Ponto de entrada FastAPI, CORS e Lifespan
│   │   ├── config.py            # Configurações tipadas via pydantic-settings
│   │   ├── database.py          # Pool de conexões do PostgreSQL (psycopg_pool)
│   │   ├── schemas/             # Contratos e validação Pydantic (Enums, Request/Response)
│   │   │   └── problem.py
│   │   ├── services/            # Camada de lógica de negócio
│   │   │   ├── gemini_service.py   # Integração com Google Gemini
│   │   │   └── problem_service.py  # Operações e queries parametrizadas SQL
│   │   └── routes/              # Endpoints REST (/problems)
│   │       └── problems.py
│   ├── tests/                   # 24 testes automatizados com Pytest
│   ├── schema.sql               # DDL para criação da tabela problems e índices
│   ├── setup_db.py              # Script utilitário para provisionamento do banco
│   ├── requirements.txt         # Dependências do backend
│   └── .env.example             # Exemplo das variáveis de ambiente
│
├── frontend/
│   ├── src/
│   │   ├── components/          # Componentes visuais (ProblemForm, ProblemCard, PriorityBadge)
│   │   ├── services/            # Cliente HTTP (fetch / api.ts)
│   │   ├── types/               # Tipagens TypeScript (Category, Priority, Problem)
│   │   ├── App.tsx              # Componente raiz com navegação por abas
│   │   └── index.css            # Estilização completa da interface
│   ├── package.json
│   └── vite.config.ts
│
├── .gitignore
└── README.md
```

---

## ⚙️ Como Executar Localmente

### 1. Pré-requisitos
- [Python 3.11+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/)
- [PostgreSQL](https://www.postgresql.org/) rodando localmente (porta 5432)
- Uma chave da API do Google Gemini ([Google AI Studio](https://aistudio.google.com/apikey))

---

### 2. Configuração do Banco e Backend

```powershell
# 1. Navegue até a pasta do backend
cd backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure o arquivo de variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env e preencha GEMINI_API_KEY e a senha do seu PostgreSQL

# 5. Crie o banco de dados e as tabelas
python setup_db.py

# 6. Execute a suíte de testes
pytest -v

# 7. Inicie o servidor FastAPI
uvicorn app.main:app --reload --port 8000
```

- A API estará rodando em: `http://localhost:8000`
- Documentação interativa Swagger: `http://localhost:8000/docs`

---

### 3. Configuração do Frontend

Abra um novo terminal:

```powershell
# 1. Navegue até a pasta do frontend
cd frontend

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento Vite
npm run dev
```

- Acesse a aplicação no seu navegador: `http://localhost:5173`

---

## 🔒 Segurança e Boas Práticas Aplicadas

- **Credenciais Protegidas**: Chaves de API e senhas nunca são versionadas no Git (protegidas via `.gitignore` e `.env`).
- **Prevenção contra SQL Injection**: Todas as instruções ao PostgreSQL utilizam consultas parametrizadas com placeholders (`%s`).
- **Validação em Múltiplas Camadas (Defense in Depth)**:
  1. Validação na entrada HTTP com Pydantic (`ProblemCreateRequest`).
  2. Validação da resposta da IA com Pydantic (`GeminiAnalysisResult`).
  3. Validação a nível de banco com `CHECK constraints` no PostgreSQL.
- **Isolamento em Testes**: Todos os testes com Pytest utilizam mocks, garantindo testes rápidos, determinísticos e sem consumo da cota da API.

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais e práticos sob a licença MIT.
