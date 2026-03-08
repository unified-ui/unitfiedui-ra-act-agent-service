"""Application configuration module."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    server_host: str = "0.0.0.0"
    server_port: int = 8086
    log_level: str = "info"

    vault_type: str = "dotenv"
    app_vault_type: str | None = None

    azure_keyvault_url: str = ""
    azure_keyvault_vault_name: str = ""

    hashicorp_vault_addr: str = ""
    hashicorp_vault_token: str = ""
    hashicorp_vault_mount_point: str = "secret"

    app_vault_key_agent_to_react_service: str = "AGENT_TO_REACT_SERVICE_KEY"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}

    @property
    def effective_app_vault_type(self) -> str:
        """Return effective app vault type, falling back to vault_type."""
        return self.app_vault_type or self.vault_type


settings = Settings()
