"""LLM Provider Abstraction Layer.

Defines a pluggable interface for LLM backends:
- BaseLLMClient: Common interface for all inference providers
- OllamaClient: Local, offline inference with quantized models (Qwen 2.5 Coder)
- AgentClient: Agent-driven inference for Antigravity IDE / headless workflows
"""

import abc
import logging
from pathlib import Path
from typing import Optional

from academy.utils import resolve_path, write_file, now_str

logger = logging.getLogger("academy")


class LLMError(Exception):
    """Base exception for LLM provider errors."""
    pass


class BaseLLMClient(abc.ABC):
    """Abstract base class for all LLM inference providers."""

    def __init__(self, config: dict):
        self.config = config

    @abc.abstractmethod
    def health_check(self) -> bool:
        """Check if the inference engine is available and responsive."""
        pass

    @abc.abstractmethod
    def is_model_available(self) -> bool:
        """Check if the configured model is ready to serve requests."""
        pass

    @abc.abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Send a generation request to the LLM backend.

        Args:
            prompt: Task/user prompt.
            system_prompt: System-level role and constraint instructions.

        Returns:
            The generated response string.
        """
        pass

    def check_cuda_conflict(self) -> Optional[str]:
        """Check for GPU/VRAM conflicts if applicable. Default returns None."""
        return None

    def warmup(self) -> bool:
        """Pre-load model weights into memory/VRAM if applicable. Default returns True."""
        return True


class AgentClient(BaseLLMClient):
    """
    Agent-driven LLM provider for Antigravity IDE / headless agent workflows.

    Prepares structured prompts into the logs directory for the AI agent to
    synthesize, avoiding local GPU/VRAM bottlenecks while ensuring deterministic
    state tracking (SM-2, syllabus parsing, archiving) remains automated.
    """

    def __init__(self, config: dict):
        super().__init__(config)
        self.logs_dir = resolve_path(config.get("paths", {}).get("logs_dir", "logs"))
        self.agent_prompt_path = self.logs_dir / "agent_prompt.md"

    def health_check(self) -> bool:
        """Agent provider is always healthy when invoked in an agentic environment."""
        return True

    def is_model_available(self) -> bool:
        """Agent backend is ready."""
        return True

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Export prompt to logs/agent_prompt.md and return an agent-ready response.
        """
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        content = (
            f"# Agent Prompt — Prepared at {now_str()}\n\n"
            f"## System Instructions\n\n{system_prompt}\n\n"
            f"## Task Prompt\n\n{prompt}\n"
        )
        write_file(self.agent_prompt_path, content)
        logger.info(f"Agent prompt prepared and exported to: {self.agent_prompt_path}")

        return (
            "<!-- SPRINT_GENERATED_BY_AGENT -->\n"
            f"> 🤖 **Agent Mode Active**: Context prompt prepared at `{self.agent_prompt_path}`.\n"
            "> The AI Agent will review this prompt and finalize active_sprint.md."
        )


def get_llm_client(config: dict, provider_override: Optional[str] = None) -> BaseLLMClient:
    """
    Factory to instantiate the appropriate LLM client based on configuration.

    Args:
        config: Loaded config.yaml dictionary.
        provider_override: Optional CLI override ('ollama' or 'agent').

    Returns:
        An instance of BaseLLMClient.
    """
    provider = provider_override or config.get("llm_provider", "ollama")
    provider = str(provider).lower().strip()

    if provider == "agent":
        logger.info("Initializing Agent LLM client (Antigravity IDE mode)")
        return AgentClient(config)

    # Default to Ollama for offline/local showcase
    from academy.ollama import OllamaClient
    logger.info("Initializing Ollama LLM client (Local inference)")
    return OllamaClient(config)
