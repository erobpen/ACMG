


from models import gpt_new

class generator:
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
    

    def generate(self, prompt, messages):
        if messages is None:
            messages = [{"role": "user", "content": prompt}]  
        else:
            messages.append({"role": "user", "content": prompt})
        response = gpt_new(messages, n=1, stop=None)[0]
        messages.append({"role": "assistant", "content": response})
        response = response.replace("```minizinc", '').replace("```", '').replace("mzn", '')
        return response, messages
    
    def add_warnings(self, first_prompt, subsequent_prompt, model, recognized, result):
        if result is None:
            return first_prompt
        return subsequent_prompt.format(model=model, recognized=recognized, warnings=result)
         
    
         