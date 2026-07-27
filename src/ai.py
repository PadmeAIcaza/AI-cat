import os
from dotenv import load_dotenv

class GeminiAI:
    """Small stateful wrapper around the Gemini chat API."""

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add your Gemini API key to that "
                "environment variable, then restart VoidCat."
            )

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "Gemini support is not installed. Run: "
                "python -m pip install -r requirements.txt"
            ) from exc

        self.client = genai.Client(api_key=api_key)
        model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.model = model
        self.chat = self.client.chats.create(model=model)

    def ask(self, prompt):
        try:
            response = self.chat.send_message(prompt)
        except Exception as exc:
            if "404" in str(exc) or "NOT_FOUND" in str(exc):
                raise RuntimeError(
                    f"The configured Gemini model ({self.model}) is unavailable. "
                    "Set GEMINI_MODEL to a model enabled for your API key."
                ) from exc
            raise
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")
        return response.text.strip()
