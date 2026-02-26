import ollama
class LLMService:
    def __init__(self, model_name = 'qwen2:7b'):
        self.model_name = model_name
    
    #   System: ...
    #   User: ...
    #   Assistant: ...
    #   User: ...
    #   Assistant: ...
    # format of messages for qwen or modern models: [{"role":"system/user/assistant", "content":"..."}]
    def generate_response(self, prompt):
        reponse = ollama.chat(
            self.model_name, 
            messages=[{"role": "user", "content": prompt}])
        return reponse['message']['content']
    
    
