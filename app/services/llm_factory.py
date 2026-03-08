"""LLM factory for creating language model instances from configuration."""

import logging

from langchain_core.language_models import BaseChatModel

from app.models import AIModelConfig

logger = logging.getLogger(__name__)

_PROVIDER_AZURE_OPENAI = "AZURE_OPENAI"
_PROVIDER_OPENAI = "OPENAI"
_PROVIDER_ANTHROPIC = "ANTHROPIC"
_PROVIDER_GOOGLE_GENAI = "GOOGLE_GENAI"
_PROVIDER_OLLAMA = "OLLAMA"
_PROVIDER_MISTRAL = "MISTRAL"
_PROVIDER_GROQ = "GROQ"


def create_llm(config: AIModelConfig) -> BaseChatModel:
    """Create a BaseChatModel instance from an AI model configuration.

    Args:
        config: AI model configuration with provider and credentials.

    Returns:
        A configured BaseChatModel instance.

    Raises:
        ValueError: If the provider is not supported.
    """
    provider = config.provider.upper()

    if provider == _PROVIDER_AZURE_OPENAI:
        return _create_azure_openai(config)
    if provider == _PROVIDER_OPENAI:
        return _create_openai(config)
    if provider == _PROVIDER_ANTHROPIC:
        return _create_anthropic(config)
    if provider == _PROVIDER_GOOGLE_GENAI:
        return _create_google_genai(config)
    if provider == _PROVIDER_OLLAMA:
        return _create_ollama(config)
    if provider == _PROVIDER_MISTRAL:
        return _create_mistral(config)
    if provider == _PROVIDER_GROQ:
        return _create_groq(config)

    msg = f"Unsupported LLM provider: {config.provider}"
    raise ValueError(msg)


def _create_azure_openai(config: AIModelConfig) -> BaseChatModel:
    """Create an Azure OpenAI chat model.

    Args:
        config: Model configuration.

    Returns:
        AzureChatOpenAI instance.
    """
    from langchain_openai import AzureChatOpenAI

    return AzureChatOpenAI(
        azure_endpoint=config.endpoint,
        azure_deployment=config.deployment_name,
        api_version=config.api_version,
        api_key=config.api_key,
    )


def _create_openai(config: AIModelConfig) -> BaseChatModel:
    """Create an OpenAI chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatOpenAI instance.
    """
    from langchain_openai import ChatOpenAI

    kwargs: dict[str, object] = {
        "model": config.model_name,
        "api_key": config.api_key,
    }
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.organization:
        kwargs["organization"] = config.organization
    return ChatOpenAI(**kwargs)  # type: ignore[arg-type]


def _create_anthropic(config: AIModelConfig) -> BaseChatModel:
    """Create an Anthropic chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatAnthropic instance.
    """
    from langchain_anthropic import ChatAnthropic

    return ChatAnthropic(model=config.model_name, api_key=config.api_key)  # type: ignore[arg-type]


def _create_google_genai(config: AIModelConfig) -> BaseChatModel:
    """Create a Google GenAI chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatGoogleGenerativeAI instance.
    """
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=config.model_name, google_api_key=config.api_key)  # type: ignore[arg-type]


def _create_ollama(config: AIModelConfig) -> BaseChatModel:
    """Create an Ollama chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatOllama instance.
    """
    from langchain_ollama import ChatOllama

    kwargs: dict[str, object] = {"model": config.model_name}
    if config.base_url:
        kwargs["base_url"] = config.base_url
    return ChatOllama(**kwargs)  # type: ignore[arg-type]


def _create_mistral(config: AIModelConfig) -> BaseChatModel:
    """Create a Mistral chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatMistralAI instance.
    """
    from langchain_mistralai import ChatMistralAI

    return ChatMistralAI(model=config.model_name, api_key=config.api_key)  # type: ignore[arg-type]


def _create_groq(config: AIModelConfig) -> BaseChatModel:
    """Create a Groq chat model.

    Args:
        config: Model configuration.

    Returns:
        ChatGroq instance.
    """
    from langchain_groq import ChatGroq

    return ChatGroq(model=config.model_name, api_key=config.api_key)  # type: ignore[arg-type]
