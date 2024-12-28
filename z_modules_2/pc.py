
from modules.mem import mc
from models import gpt_new

class pc:

    def __init__(self):
        # print("pc initialised")
        pass
        
    def fetch_data(self, prompt_id, mc : mc) -> dict:
        return mc.return_data(prompt_id)

    def get_user_prompt(self) -> str:
        lines = []
        while True:
            try:
                line = input(">> ")
                if line == '':
                    break
            except EOFError:
                break
            lines.append(line)
        return '\n'.join(lines)

    def get_llm_response(self, prompt: str, messages) -> dict:
        if messages is None:
            messages = [{"role": "user", "content": prompt}]  
        else:
            messages.append({"role": "user", "content": prompt})
        response = gpt_new(messages, n=1, stop=None)[0]
        messages.append({"role": "assistant", "content": response})
        return response, messages


    def format_prompt(self, prompt: str, task=None, input=None) -> str:
        return prompt.format(task=task, input=input)