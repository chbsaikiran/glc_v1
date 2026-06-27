"""Groq Whisper Large v3 Turbo Speech-to-Text provider adapter.

Connects to the Groq Cloud STT API using httpx, sending audio data
via multipart form-data, and returning a canonical TranscribeResult.
"""

from __future__ import annotations

import json
import os

import httpx

from glc.voice.stt.base import STTError, STTProvider, TranscribeResult
from glc.voice.stt.providers.groq_whisper.schemas import GroqVerboseJsonResponse

# API Configuration Constants
GROQ_STT_URL = "https://api.groq.com/openai/v1/audio/transcriptions"
DEFAULT_MODEL = "whisper-large-v3-turbo"
RESPONSE_FORMAT = "verbose_json"
REQUEST_TIMEOUT_SECONDS = 30.0

# Mapping of common language names to ISO 639-1 language codes
LANG_NAME_TO_CODE = {
    "english": "en",
    "spanish": "es",
    "french": "fr",
    "german": "de",
    "italian": "it",
    "japanese": "ja",
    "chinese": "zh",
    "portuguese": "pt",
    "russian": "ru",
    "korean": "ko",
}


class Provider(STTProvider):
    """Groq Whisper Speech-to-Text provider implementation."""

    name = "groq_whisper"

    async def transcribe(self, audio: bytes, mime: str) -> TranscribeResult:
        """Transcribe audio bytes using the Groq Whisper API.

        If a mock is provided in the configuration, delegates directly
        to the mock provider.
        """
        # Test Mock Delegation
        mock_provider = self.config.get("mock")
        if mock_provider is not None:
            return await mock_provider.transcribe(audio, mime)

        # Validate input
        self._validate_input(audio, mime)

        # Return empty result immediately for empty audio
        if len(audio) == 0:
            return TranscribeResult(
                text="",
                language="en",
                duration_ms=0,
                provider=self.name,
                cost_usd=0.0,
            )

        # Load configuration
        api_key, model = self._load_config()

        # Build payload
        files, data = self._build_payload(audio, mime, model)

        # Execute request
        response = await self._execute_request(api_key, files, data)

        # Validate and parse response
        parsed_response = self._validate_and_parse_response(response)

        # Convert to canonical result
        return self._convert_response(parsed_response)

    def _validate_input(self, audio: bytes, mime: str) -> None:
        """Validate that input types match the expected signatures."""
        if not isinstance(audio, bytes):
            raise STTError("audio must be of type bytes", status=400)
        if not mime or not isinstance(mime, str):
            raise STTError("MIME type must be a non-empty string", status=400)

    def _load_config(self) -> tuple[str, str]:
        """Load API key and target model from environment or config."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise NotImplementedError("GROQ_API_KEY environment variable is not set")

        model = os.getenv("GLC_GROQ_STT_MODEL") or self.config.get("model") or DEFAULT_MODEL
        return api_key, model

    def _build_payload(self, audio: bytes, mime: str, model: str) -> tuple[dict, dict]:
        """Build the files and data payload for the multipart request."""
        # Determine extension from MIME type
        ext = "wav"
        if "mpeg" in mime or "mp3" in mime:
            ext = "mp3"
        elif "ogg" in mime:
            ext = "ogg"
        elif "webm" in mime:
            ext = "webm"
        elif "flac" in mime:
            ext = "flac"
        elif "mp4" in mime:
            ext = "mp4"
        elif "m4a" in mime:
            ext = "m4a"

        files = {
            "file": (f"audio.{ext}", audio, mime),
        }
        data = {
            "model": model,
            "response_format": RESPONSE_FORMAT,
        }
        return files, data

    async def _execute_request(self, api_key: str, files: dict, data: dict) -> httpx.Response:
        """Dispatch the POST request using httpx."""
        headers = {
            "Authorization": f"Bearer {api_key}",
        }
        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                return await client.post(GROQ_STT_URL, headers=headers, files=files, data=data)
        except httpx.TimeoutException as e:
            raise STTError(f"HTTP request to Groq timed out: {e}", status=504) from e
        except httpx.RequestError as e:
            raise STTError(f"Network error communicating with Groq: {e}", status=502) from e

    def _validate_and_parse_response(self, response: httpx.Response) -> GroqVerboseJsonResponse:
        """Validate HTTP response code, parse JSON, and load into Pydantic model."""
        if response.status_code != 200:
            raise STTError(
                f"Groq API returned error {response.status_code}: {response.text}",
                status=response.status_code,
            )

        try:
            res_json = response.json()
        except json.JSONDecodeError as e:
            raise STTError(f"Malformed JSON response from Groq: {e}", status=502) from e

        try:
            return GroqVerboseJsonResponse.model_validate(res_json)
        except Exception as e:
            raise STTError(f"Unexpected response schema from Groq: {e}", status=502) from e

    def _convert_response(self, parsed: GroqVerboseJsonResponse) -> TranscribeResult:
        """Convert a validated Groq response schema into a canonical TranscribeResult."""
        duration_sec = parsed.duration or 0.0
        duration_ms = int(duration_sec * 1000)

        raw_lang = (parsed.language or "en").lower()
        lang = LANG_NAME_TO_CODE.get(raw_lang, raw_lang)

        return TranscribeResult(
            text=parsed.text,
            language=lang,
            duration_ms=duration_ms,
            provider=self.name,
            cost_usd=0.0,
        )
