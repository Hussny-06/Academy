"""Ollama HTTP API Client.

Handles communication with the local Ollama instance running in WSL.
Single-call design: one prompt in, one response out.
"""

import logging
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

logger = logging.getLogger("academy")


class OllamaError(Exception):
    """Raised when Ollama communication fails."""
    pass


class OllamaClient:
    """Client for the Ollama REST API."""

    def __init__(self, config: dict):
        self.base_url = config.get("ollama_url", "http://localhost:11434")
        self.model = config.get("model", "qwen2.5-coder:14b")
        self.context_window = config.get("context_window", 8192)
        self.temperature = config.get("temperature", 0.3)
        self.timeout = config.get("request_timeout_sec", 120)

    def health_check(self) -> bool:
        """Check if Ollama is running and responsive."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except (ConnectionError, Timeout):
            return False

    def is_model_available(self) -> bool:
        """Check if the configured model is pulled."""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if resp.status_code != 200:
                return False
            models = resp.json().get("models", [])
            # Match by model name (ignoring tag variations)
            model_base = self.model.split(":")[0]
            for m in models:
                if model_base in m.get("name", ""):
                    return True
            return False
        except (ConnectionError, Timeout, RequestException):
            return False

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Send a single generation request to Ollama.

        Args:
            prompt: The user/task prompt.
            system_prompt: Optional system-level instructions.

        Returns:
            The model's response text.

        Raises:
            OllamaError: If the request fails.
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_ctx": self.context_window,
                "temperature": self.temperature,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        logger.info(
            f"Calling Ollama: model={self.model}, "
            f"prompt_len={len(prompt)}, ctx={self.context_window}"
        )

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            if resp.status_code != 200:
                error_body = resp.text[:500]
                logger.error(f"Ollama returned {resp.status_code}: {error_body}")
                raise OllamaError(
                    f"Ollama returned {resp.status_code}: {error_body}"
                )

            data = resp.json()
            response_text = data.get("response", "")

            # Log token stats if available
            total_duration = data.get("total_duration", 0)
            eval_count = data.get("eval_count", 0)
            if total_duration > 0 and eval_count > 0:
                tokens_per_sec = eval_count / (total_duration / 1e9)
                logger.info(
                    f"Ollama response: {eval_count} tokens, "
                    f"{tokens_per_sec:.1f} tok/s, "
                    f"{total_duration / 1e9:.1f}s total"
                )

            return response_text

        except ConnectionError:
            raise OllamaError(
                "Cannot connect to Ollama. Is it running? "
                f"Expected at {self.base_url}\n"
                "Start it with: ollama serve (in WSL)"
            )
        except Timeout:
            raise OllamaError(
                f"Ollama request timed out after {self.timeout}s. "
                "The model may be too slow or the prompt too long."
            )
        except RequestException as e:
            raise OllamaError(f"Ollama request failed: {e}")
