import os
from openai import OpenAI
from config.settings import LLM_MODEL

class LLMService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or LLM_MODEL
        base_url = os.getenv("LLM_BASE_URL", "http://llama-server:8080/v1")
        
        self.client = OpenAI(base_url=base_url, api_key="dummy")
        print(f"[LLM] Using llama.cpp at: {base_url}")
        print(f"[LLM] Model: {self.model_name}")

    def generate_response(self, query: str, context: str = "", mode="qa") -> str:
        if mode == "summary":
            system_prompt = """
You are an AI specialized in summarizing documents.
Rules:
- Only use information from the CONTEXT.
- Summarize the main content of the document.
- Do not add information outside the CONTEXT.
- Answer in the SAME LANGUAGE as the user's question.
"""
        else:
            system_prompt = """
You are an AI assistant that answers questions based on the provided document.
Rules:
- Only use information from the CONTEXT.
- If CONTEXT doesn't contain the answer, say: "I couldn't find information in the document."
- Do not make assumptions.
- Answer in the SAME LANGUAGE as the user's question.
"""

        user_prompt = f"""
CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"[LLM ERROR]: {e}")
            return f"Lỗi Ollama: {str(e)}"
