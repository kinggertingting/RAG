import ollama
from config.settings import LLM_MODEL


class LLMService:

    def __init__(self, model_name: str = None):
        self.model_name = model_name or LLM_MODEL

    def generate_response(self, query: str, context: str = "") -> str:

        system_prompt = f"""
        Bạn là trợ lý AI chuyên trả lời dựa trên tài liệu được cung cấp.

        QUY TẮC:
        - Chỉ được trả lời dựa trên thông tin trong ngữ cảnh.
        - Nếu ngữ cảnh không chứa thông tin để trả lời, hãy nói:
        "Tôi không tìm thấy thông tin trong tài liệu."
        - Không được tự suy đoán hoặc sử dụng kiến thức bên ngoài.
        

        

        Ngữ cảnh:
        {context}

        Câu hỏi:
        {query}
        """
        user_prompt = f"{query}"
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
                    "num_predict": 512
                }
            )

            return response["message"]["content"]

        except Exception as e:
            return f"Lỗi khi gọi LLM: {str(e)}"