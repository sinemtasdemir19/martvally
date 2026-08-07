import requests

from config import Config


class AIServiceError(Exception):
    """Raised when the AI service cannot generate a response."""
    pass


class AIService:

    def __init__(self):
        self.api_key = Config.GROQ_API_KEY
        self.model = "llama-3.1-8b-instant"
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.business_context = Config.BUSINESS_CONTEXT

    def build_messages(self, user_message, history=None):
        """
        Builds the message list that will be sent to the AI provider.
        """

        messages = [
            {
                "role": "system",
                "content": self.business_context,
            }
        ]

        if history:
            messages.extend(history[-10:])

        messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )

        return messages

    def call_model(self, messages):
        """
        Sends the prepared messages to the Groq API
        and returns the raw JSON response.
        """

        if not self.api_key:
            return {
                "demo_mode": True,
                "content": (
                    "Martvally is currently running in demo mode. "
                    "The AI service has not been configured yet."
                ),
            }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": messages,
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            raise AIServiceError(
                "Unable to communicate with the AI service."
            ) from error

    def validate_response(self, result):
        """
        Validates the AI provider response
        and extracts the assistant message.
        """

        if result.get("demo_mode"):
            return result["content"]

        try:
            content = result["choices"][0]["message"]["content"]

        except (KeyError, IndexError, TypeError) as error:
            raise AIServiceError(
                "The AI service returned an invalid response."
            ) from error

        if not content or not content.strip():
            raise AIServiceError(
                "The AI service returned an empty response."
            )

        return content.strip()

    def generate_response(self, user_message, history=None):
        """
        Coordinates the complete AI response generation process.
        """

        if not user_message or not user_message.strip():
            raise AIServiceError(
                "User message cannot be empty."
            )

        messages = self.build_messages(
            user_message=user_message,
            history=history,
        )

        result = self.call_model(messages)

        return self.validate_response(result)


ai_service = AIService()