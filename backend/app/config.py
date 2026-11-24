from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas a partir de variáveis de ambiente ou arquivo .env.
    O Pydantic Settings valida tipos e avisa imediatamente se algo obrigatório faltar.
    """
    # Google Gemini API
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"

    # PostgreSQL Database
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "assistente_ti"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = ""

    # Servidor
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        """Retorna a string de conexão no formato padrão do PostgreSQL."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


# Instância única compartilhada na aplicação (Singleton pattern)
settings = Settings()
