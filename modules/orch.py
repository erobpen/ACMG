

from mem import mem
from models import gpt_new

import time
import threading

class orch:

    def __init__(self, minizinc_solver, recognizer, generator, mem : mem):
        self.minizinc_solver = minizinc_solver
        self.recognizer = recognizer
        self.generator = generator
        self.mem = mem
        # print("pc initialised")
        pass

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
    
    def get_llm_response(self, prompt: str, model, messages) -> dict:
        # print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
        print(type(model).__name__)

        # temporarily set messages to None
        # messages = None

        response, messages = model.get_response(prompt, messages)

        return response, messages


    def fetch_control_prompt(self, prompt_id) -> str:
        try:
            data = self.mem.return_data(prompt_id)
            return data
        except Exception as e:
            return False
    
    def fetch_data(self, prompt_id) -> str:
        try:
            data = self.mem.return_data(prompt_id)
            return data
        except Exception as e:
            return False
    
    def fetch_model(self, prompt_id) -> str:
        return self.mem.return_data("stored_models")[prompt_id]
    
    

