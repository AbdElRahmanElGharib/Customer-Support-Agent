import requests
from django.conf import settings

class LLMServiceError(Exception):
    pass

class LocalLLMService:
    def generate_answer(self, question, context_chunks):
        context = '\n\n'.join(context_chunks)

        prompt = f"""You are a precise assistant.
            Answer ONLY using the context below.

            Context:
            {context}

            Question:
            {question}

            Answer:"""
        
        url = f'{settings.LLM_SERVICE_BASE_URL}/api/'
        payload = {'message': prompt}

        try:
            response = requests.post(url, json=payload, timeout=30)
        except requests.RequestException as exc:
            raise LLMServiceError('Failed to reach LLM service') from exc

        if response.status_code != 200:
            raise LLMServiceError(
                f'LLM service error: {response.status_code} - {response.text}'
            )

        data = response.json()
        return data['response']
