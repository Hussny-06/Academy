"""Ollama HTTP API Client.

Handles communication with the local Ollama instance.
Single-call design: one prompt in, one response out.

Includes pre-flight checks for CUDA conflicts and model warmup.
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
        self.timeout = config.get("request_timeout_sec", 300)

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

    def check_running_models(self) -> list:
        """
        Check which models are currently loaded in Ollama (GET /api/ps).

        Returns:
            List of dicts with info about running models, or empty list.
        """
        try:
            resp = requests.get(f"{self.base_url}/api/ps", timeout=5)
            if resp.status_code == 200:
                return resp.json().get("models", [])
        except (ConnectionError, Timeout, RequestException):
            pass
        return []

    def check_cuda_conflict(self) -> str | None:
        """
        Detect potential CUDA conflicts from other Ollama sessions.

        Returns:
            Warning message string if conflict detected, None if all clear.
        """
        running = self.check_running_models()
        if not running:
            return None

        for model_info in running:
            model_name = model_info.get("name", "unknown")
            size_vram = model_info.get("size_vram", 0)
            # If a different model is loaded, or the same model is already active
            # from an interactive session, there could be a CUDA memory issue
            if size_vram > 0:
                vram_gb = size_vram / (1024 ** 3)
                return (
                    f"⚠️  CUDA conflict risk: '{model_name}' is already loaded "
                    f"({vram_gb:.1f} GB VRAM). If you have an 'ollama run' session "
                    f"open, close it first (type /bye) to free GPU memory."
                )

        return None

    def warmup(self) -> bool:
        """
        Pre-load the model into VRAM by sending a minimal prompt.

        This avoids cold-start delays on the first real request.
        The 14B model can take 2-3 minutes to load on a 6GB GPU.

        Returns:
            True if warmup succeeded, False on failure.
        """
        logger.info(f"Warming up model '{self.model}' (loading into VRAM)...")

        payload = {
            "model": self.model,
            "prompt": "Hello",
            "stream": False,
            "options": {
                "num_ctx": 128,  # Minimal context for warmup
                "num_predict": 1,  # Generate just 1 token
            },
        }

        try:
            resp = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                total_duration = data.get("total_duration", 0)
                load_duration = data.get("load_duration", 0)
                logger.info(
                    f"Warmup complete: model loaded in "
                    f"{load_duration / 1e9:.1f}s, "
                    f"total {total_duration / 1e9:.1f}s"
                )
                return True
            else:
                error_body = resp.text[:300]
                logger.error(f"Warmup failed ({resp.status_code}): {error_body}")
                return False
        except (ConnectionError, Timeout, RequestException) as e:
            logger.error(f"Warmup failed: {e}")
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

                # Detect CUDA errors specifically
                if "CUDA" in error_body or "shared object" in error_body:
                    raise OllamaError(
                        f"GPU/CUDA error detected. This usually means another "
                        f"Ollama session is using the GPU.\n"
                        f"Fix: Close any 'ollama run' sessions (type /bye), "
                        f"then retry.\n\nRaw error: {error_body}"
                    )

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
                "Start Ollama Desktop or run: ollama serve"
            )
        except Timeout:
            raise OllamaError(
                f"Ollama request timed out after {self.timeout}s. "
                "The model may still be loading into VRAM. "
                "Try running: python orchestrator.py --warmup"
            )
        except RequestException as e:
            raise OllamaError(f"Ollama request failed: {e}")
