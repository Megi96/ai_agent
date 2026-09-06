# Voice Module (Phase 5 — reserved)

This module is reserved for future voice interaction features:

- **STT (Speech-to-Text):** OpenAI Whisper or browser Web Speech API
- **TTS (Text-to-Speech):** ElevenLabs, browser SpeechSynthesis, or similar

## Planned interface

```python
class VoiceService:
    async def transcribe(self, audio_bytes: bytes) -> str: ...
    async def synthesize(self, text: str) -> bytes: ...
```

Wire into the chat flow as an optional input/output channel alongside the web UI.
