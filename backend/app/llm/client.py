"""
LLM Client integration module for ARAKNO-AI.
Supports NVIDIA Nemotron (via integrate.api.nvidia.com), OpenRouter, Ollama, and Gemini.
"""

from typing import Optional, Dict, Any, AsyncGenerator, Tuple
from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class LLMClient:
    """Unified client for optional LLM completions."""

    def __init__(self):
        self.settings = get_settings()

    @property
    def is_enabled(self) -> bool:
        """Check if an LLM provider is active and configured."""
        if self.settings.llm_provider in ("none", "", None):
            return False
        if self.settings.llm_provider in ("nvidia", "openrouter", "gemini"):
            return bool(self.settings.llm_api_key)
        if self.settings.llm_provider == "ollama":
            return True
        return False

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        enable_thinking: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 4096,
    ) -> Tuple[str, str]:
        """
        Generate completion from configured LLM provider.
        Returns a tuple of (content, reasoning).
        """
        if not self.is_enabled:
            return "", ""

        provider = self.settings.llm_provider
        api_key = self.settings.llm_api_key
        model = self.settings.llm_model

        try:
            from openai import AsyncOpenAI

            base_url = None
            extra_body = None

            if provider == "nvidia":
                base_url = self.settings.llm_base_url or "https://integrate.api.nvidia.com/v1"
                model = model or "nvidia/nemotron-3-ultra-550b-a55b"
                if enable_thinking:
                    extra_body = {"chat_template_kwargs": {"enable_thinking": True}}
            elif provider == "openrouter":
                base_url = self.settings.llm_base_url or "https://openrouter.ai/api/v1"
                model = model or "meta-llama/llama-3.2-3b-instruct:free"
            elif provider == "ollama":
                base_url = self.settings.llm_base_url or "http://localhost:11434/v1"
                api_key = api_key or "ollama"
                model = model or "llama3.2"
            else:
                logger.warning(f"Unsupported LLM provider: {provider}")
                return "", ""

            client = AsyncOpenAI(base_url=base_url, api_key=api_key)

            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})

            kwargs: Dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }
            if extra_body:
                kwargs["extra_body"] = extra_body

            response_stream = await client.chat.completions.create(**kwargs)

            reasoning_chunks = []
            content_chunks = []

            async for chunk in response_stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                reasoning = getattr(delta, "reasoning_content", None)
                if reasoning:
                    reasoning_chunks.append(reasoning)
                if delta.content is not None:
                    content_chunks.append(delta.content)

            full_content = "".join(content_chunks)
            full_reasoning = "".join(reasoning_chunks)

            return full_content, full_reasoning

        except Exception as e:
            logger.error("LLM completion error", provider=provider, error=str(e))
            return f"[LLM generation failed: {str(e)}]", ""
