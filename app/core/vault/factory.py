"""Vault factory for creating vault instances based on configuration."""

from app.core.vault.base import BaseVault


def create_vault(vault_type: str, **kwargs: str) -> BaseVault:
    """Create a vault instance based on the vault type.

    Args:
        vault_type: Type of vault ('dotenv', 'azure_keyvault', 'hashicorp_vault').
        **kwargs: Additional arguments for the vault constructor.

    Returns:
        A vault instance.

    Raises:
        ValueError: If the vault type is not supported.
    """
    vault_type_lower = vault_type.lower()

    if vault_type_lower == "dotenv":
        from app.core.vault.dotenv_vault import DotEnvVault

        return DotEnvVault()

    if vault_type_lower == "azure_keyvault":
        from app.core.vault.azure_keyvault import AzureKeyVault

        vault_url = kwargs.get("vault_url", "")
        if not vault_url:
            msg = "Azure Key Vault URL is required"
            raise ValueError(msg)
        return AzureKeyVault(vault_url=vault_url)

    if vault_type_lower == "hashicorp_vault":
        from app.core.vault.hashicorp_vault import HashiCorpVault

        return HashiCorpVault(
            addr=kwargs.get("addr", ""),
            token=kwargs.get("token", ""),
            mount_point=kwargs.get("mount_point", "secret"),
        )

    msg = f"Unsupported vault type: {vault_type}"
    raise ValueError(msg)
