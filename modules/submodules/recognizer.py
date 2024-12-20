

from models import gpt_new

class recognizer:
    def __init__(self):
        pass

    def get_response(self, prompt: str, messages):
            if messages is None:
                messages = [{"role": "user", "content": prompt}]  
            else:
                messages.append({"role": "user", "content": prompt})
            response = gpt_new(messages, n=1, stop=None)[0]
            messages.append({"role": "assistant", "content": response})
            return response, messages