import os
from dotenv import load_dotenv
from pathlib import Path

class GeminiAI:
    def __init__(self):
        # load environment variables
        load_dotenv()
        # get API key
        api_key = os.getenv("GEMINI_API_KEY")

        # validate API key
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not set. Add your Gemini API key to that environment variable, then restart VoidCat.")

        try:
            # import Gamini SDK
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("Gemini support is not installed. Run: ""python -m pip install -r requirements.txt") from exc

        # create Gemini client
        self.client = genai.Client(api_key=api_key)

        # choose model
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

        # load personality from file
        personality = self.load_personality()

        # create succesful chat with personality
        self.chat = self.client.chats.create(model=self.model, config=types.GenerateContentConfig(system_instruction=personality))

    @staticmethod
    def load_personality():
        personality_path = (Path(__file__).resolve().parent / "personality.txt")

        try:
            personality = personality_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise RuntimeError(f"VoidCat's personality file was not found at {personality_path}.") from exc

        if not personality:
            raise RuntimeError("VoidCat's personality file is empty.")

        return personality

    def ask(self, prompt):
        try:
            # send prompt through existing chat
            response = self.chat.send_message(prompt)
        except Exception as exc:
            # validate response
            if "404" in str(exc) or "NOT_FOUND" in str(exc):
                raise RuntimeError(
                    f"The configured Gemini model ({self.model}) is unavailable. Set GEMINI_MODEL to a model enabled for your API key.") from exc
            if "429" in str(exc) or "RESOURCE_EXHAUSTED" in str(exc):
                raise RuntimeError("VoidCat needs a short catnap because the Gemini request limit was reached. Please try again in about one minute.") from exc

            raise

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()