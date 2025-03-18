
from models import gpt_new

# extracts relevant semantic entities from the paresed the Model (not task)
class recognizer():

    def __init__(self):

        #recognizer
        self.id = "ft:gpt-4o-mini-2024-07-18:personal::AZaboB4q"

        # self.id = "gpt-4o-mini-2024-07-18"
    
    def get_response(self, prompt: str, messages) -> dict:
         
         return get_gateway_response(self.id, prompt, messages)

#generates MiniZinc model based on output from the Recignizer and control prompt
class generator():
    def __init__(self):

        # generator
        self.id = "ft:gpt-4o-mini-2024-07-18:personal::AZaW0y5H"

        # self.id = "gpt-4o-mini-2024-07-18"
    
    def get_response(self, prompt: str, messages) -> dict:
         
         return get_gateway_response(self.id, prompt, messages)

#parses user input mesage into the Task and the Model
class parser():

#this is wrong, recognizer does this not parser
    # odvajati tasks, model
    # izvlaciti semanticke entitete

    def __init__(self):

        # parser
        self.id = "ft:gpt-4o-mini-2024-07-18:personal::AZaTc6po"

        # self.id = "gpt-4o-mini-2024-07-18"
    
    def get_response(self, prompt: str, messages) -> dict:
         
         return get_gateway_response(self.id, prompt, messages)

class base_model():
    def __init__(self):
        self.id = "gpt-4o-mini-2024-07-18"

    def get_response(self, prompt: str, messages) -> dict:
         
         return get_gateway_response(self.id, prompt, messages)
    


def get_gateway_response(id : str, prompt: str, messages) -> dict:
        
        if messages is None:
                    messages = [{"role": "user", "content": prompt}]
        else:
            messages.append({"role": "user", "content": prompt})
        messages = messages[-18:]
        response = gpt_new(messages, model=id, n=1, stop=None)[0]
        messages.append({"role": "assistant", "content": response})
    
        return response, messages


# class recognizer():

#     def __init__(self):
#         self.id = "ft:gpt-3.5-turbo-0125:personal::AWqPKV4b"
#         # self.id = "gpt-3.5-turbo"

#    def get_response(self, prompt: str, messages) -> dict:
#            
#            return get_gateway_response(self.id, prompt, messages)


# class generator():
#     def __init__(self):
#         self.id = "ft:gpt-3.5-turbo-0125:personal::AWqFX3C0"
#         # self.id = "gpt-3.5-turbo"


#     def get_response(self, prompt: str, messages) -> dict:
#         
#         return get_gateway_response(self.id, prompt, messages)

# class parser():

#     # odvajati tasks, model
#     # izvlaciti semanticke entitete

#     def __init__(self):
#         self.id = "ft:gpt-3.5-turbo-0125:personal::AWqSSqaU"
#         # self.id = "gpt-3.5-turbo"


#     def get_response(self, prompt: str, messages) -> dict:
#         
#         return get_gateway_response(self.id, prompt, messages)

# class base_model():
#     def __init__(self):
#         # self.id = "gpt-3.5-turbo"

#         #generator
#         self.id = "gpt-3.5-turbo"

#     def get_response(self, prompt: str, messages) -> dict:
#         
#         return get_gateway_response(self.id, prompt, messages)




