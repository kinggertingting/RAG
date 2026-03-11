from openai import OpenAI
from config.settings import LLM_BASE_URL, LLM_MODEL

client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key="sk-no-key-required"
)

class RewriteQuery:
    def rewrite_query(self, query: str):

        prompt = f"""
Rewrite the following question to improve search retrieval.

Question:
{query}

Rewrite:
"""

        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        return response.choices[0].message.content