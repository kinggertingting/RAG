import ollama
from config.settings import LLM_MODEL


class LLMService:

    def __init__(self, model_name: str = None):
        self.model_name = model_name or LLM_MODEL

    def generate_response(self, query: str, context: str = "") -> str:

        system_prompt = """
Bạn là trợ lý AI trả lời câu hỏi dựa trên tài liệu được cung cấp.

Quy tắc:
- Chỉ được sử dụng thông tin trong CONTEXT.
- Nếu CONTEXT không chứa câu trả lời, hãy nói:
"Tôi không tìm thấy thông tin trong tài liệu."
- Không được tự suy đoán.
"""

        user_prompt = f"""
CONTEXT:
{context}

QUESTION:
{query}

ANSWER:
"""

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                options={
                    "temperature": 0.2,
                    "top_p": 0.9,
                    "num_predict": 150                }
            )

            return response["message"]["content"]

        except Exception as e:
            return f"Lỗi khi gọi LLM: {str(e)}"