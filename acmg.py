
import sys
import os, time, re, pandas, json
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path1 = dir_path + '\\models'
dir_path2 = dir_path + '\\modules'
sys.path.insert(0, dir_path1)
sys.path.insert(0, dir_path2)   
from modules import ai_models
from modules.orch import orch 
from modules.mem import mem
from modules.submodules.tree import node
from modules.submodules.recognizer import recognizer
from modules.submodules.generator import generator
from modules.submodules.minizinc_solver import minizinc_solver

from enum import Enum

class ParsedMessageType(Enum):
    TASK = 'Task'
    MODEL = 'Model'
    BOTH = 'Both'
    NONE = 'None'

def filter_string(input_string):
    pattern = r'[a-zA-Z0-9_]+'
    matches = re.findall(pattern, input_string)
    filtered_string = ''.join(matches)
    return filtered_string

def parse_conversation(input_string):
    """
    Parse a conversation string into a list of dictionaries with role and content.
    
    Args:
        input_string (str): A string containing conversation turns marked with 'Bot:' and 'Me:'
    
    Returns:
        list: A list of dictionaries with 'role' and 'content' keys
    """
    # Split the input string by 'Bot:' or 'Me:'
    turns = []
    current_parts = input_string.split('Bot:')[1:] + input_string.split('Me:')[1:]
    
    # Process Bot: turns
    for part in input_string.split('Bot:')[1:]:
        turns.append({
            'role': 'assistant',
            'content': part.split('Me:')[0].strip()
        })
    
    # Process Me: turns
    for part in input_string.split('Me:')[1:]:
        turns.append({
            'role': 'user',
            'content': part.split('Bot:')[0].strip()
        })
    
    # Sort the turns based on their original order
    return sorted(turns, key=lambda x: input_string.index(x['content']))

class acmg:

    def __init__(self):
        minizinc_solver1 = minizinc_solver()
        recognizer1 = recognizer()
        generator1 = generator()
        self.mem = mem()

        self.parser_model = ai_models.parser()
        self.recognizer_model = ai_models.recognizer()
        self.generator_model = ai_models.generator()
        self.base_model = ai_models.base_model()

        self.orch = orch(minizinc_solver1, recognizer1, generator1, self.mem)
        self.user_input = None
        self.task = None
        self.task_dzn = None
        self.model = None
        self.model_name = None
        self.messages = None
        pass #why this command?

    def set_models(self, models):
        self.recognizer_model = models[0]
        self.generator_model = models[1]
        self.parser_model = models[2]
        self.base_model = models[3]
    
    
    def start_execution(self, text, experiment_number, index, messages):

        self.messages = messages
        self.task = None
        self.task_dzn = None
        self.model = None

        # self.user_input = self.pc.get_user_prompt()
        self.user_input = text
        # prompt should be called control_prompt
        prompt = self.orch.fetch_control_prompt("assess_user_input")

        # STEP 1: determine the contents of hte user input
        provided, self.messages = self.orch.get_llm_response(prompt.format(input=self.user_input), self.parser_model, self.messages)
        print("Provided: \n", provided)

        # STEP 2: determine the task and model
        if provided == ParsedMessageType.TASK:
            # zatrazi model
            self.task = self.user_input
            print("Enter the problem rules:")
            # self.model = self.pc.get_user_prompt()
            self.model = self.user_input
        elif provided == ParsedMessageType.MODEL:
            # zatrazi task
            self.model = self.user_input
            print("Enter the problem input information:")
            # self.task = self.pc.get_user_prompt()
            self.task = self.user_input
        elif provided == ParsedMessageType.BOTH:
            self.subroutine_both()
        elif provided == ParsedMessageType.NONE:
            # return False
            self.task = self.user_input
            self.model = self.user_input
            self.subroutine_both()
        
        prompt_generate = self.orch.fetch_control_prompt("generate")
        subsequent_prompt = self.orch.fetch_control_prompt("generate_again")
        prompt_recognize = self.orch.fetch_control_prompt("recognize").format(input=self.model)
        prompt_reformat = self.orch.fetch_control_prompt("input_preparation")

        # naming of the model

        stored_models = self.orch.fetch_data("stored_models")
        text = "\n".join([key for key in stored_models.keys()])
        prompt = self.orch.fetch_control_prompt("classify_model")
        classification, self.messages = self.orch.get_llm_response(prompt.format(stored_models=text, input=self.user_input), self.recognizer_model, self.messages)
        classification = "false"

        # this shold be the given model name
        print("Already existing: ", classification)

        if ('false' not in classification and 'False' not in classification):
            # model exists and can be used as well as the task format
            self.model_name = classification
            
            prompt = self.orch.fetch_control_prompt(self.model_name + "_reformat")
            self.task_dzn, self.messages = self.orch.get_llm_response(prompt.format(input=self.task), self.base_model, self.messages)
            # print("Reformated task: ", self.task_dzn)

        else:
            # model does not exist and needs to be created, task formatting is created based on the minizinc model
            self.model_name, self.messages = self.orch.get_llm_response(self.orch.fetch_control_prompt("name_model").format(input=self.model), self.base_model, self.messages)
            status = False
            results = []
            minizinc_models = ""
            warnings = None

            for i in range(3):

                # STEP 3
                # recognizer extracts relevant semantic entities from the model part of the prompt
                recognized, self.messages = self.orch.get_llm_response(prompt_recognize, self.recognizer_model, self.messages)
                prompt = prompt_generate.format(model=self.model, recognized=recognized)
                result = None
                warnings = None

                
                # STEP 4: generate (3 attempts)
                for j in range(3):
                    # print("=========================================================================")
                    print("Warnings for attempt " + str(j + 1) + ": ", warnings)
                    prompt = self.orch.generator.add_warnings(prompt, subsequent_prompt, self.model, recognized, warnings)
                    mini_zinc_model, self.messages = self.orch.get_llm_response(prompt, self.generator_model, self.messages)
                    # print(prompt)

                    # STEP 7: required input preparation for testing the minizinc model
                    self.task_dzn, self.messages = self.orch.get_llm_response(prompt_reformat.format(model=mini_zinc_model, input=self.task), self.generator_model, self.messages)
                    self.orch.mem.store_new_format(self.model_name + "_reformat", self.task)

                    # STEP 5: evaluate
                    status, result, warnings = self.orch.minizinc_solver.evaluate(mini_zinc_model, self.model_name, self.task_dzn)
                    print("-"*50)
                    # print("\n\nminizinc model:\n", mini_zinc_model)
                    print(f"Result: \n{result}")
                    try:
                        print(f"Result.status: {str(result.status)}")
                    except Exception as e:
                        pass
                    print("-"*50)
                    if result != None:
                        # with open(str(index + 1) + ".txt", "a") as file2:
                        #     file2.write(mini_zinc_model)
                        #     file2.write("\n\n")
                        #     file2.write(self.task_dzn)
                        minizinc_models += str(result) + "\n___________\n"
                        minizinc_models += mini_zinc_model + "\n___________\n"
                        
                        minizinc_models += self.task_dzn + "\n" + "="*30
                        try:
                            results.append({"attempt" : str(i) + "_" + str(j), "status" : status, "solutions" : str(result)})
                        except Exception as e:
                            results.append({"attempt" : str(i) + "_" + str(j), "status" : status, "solutions" : "None"})   

                    if (result != None):
                        print("Satisfiable: ", result.status)
                    if (result != None) and (str(result.status) == 'SATISFIED'):

                        # STEP 6: store the model
                        self.orch.mem.store_new_model(self.model_name, mini_zinc_model)
                        break
                    # n = input(">>>>> ")
                
                if (result != None) and (str(result.status) == 'SATISFIED'):
                    print("CONDITION MET")
                    break

            # for a single problem, store the results
            # --------------------------------------------------------------------------------------------------------------  
            print("-" * 50)
            print("FILENAME: " + "rezultati\\" + history + "_" + "experiment_" + str(experiment_number) +"_problem_" + str(index) +  ".txt")
            print("-" * 50)
            with open("rezultati\\" + history + "_" + "experiment_" + str(experiment_number) +"_problem_" + str(index) +  ".txt", "w") as file:
                json.dump(results, file)
                
                if results == []:
                    print("No results\n")
            with open("rezultati\\" + history + "_" + "experiment_" + str(experiment_number) +"_problem_" + str(index) +  ".txt", "a") as file:
                file.write("\n\n")
                file.write(minizinc_models)
             # --------------------------------------------------------------------------------------------------------------
            
        # STEP 8: solve the problem

        # minizinc_model = self.pc.fetch_model(self.model_name)
        minizinc_model = mini_zinc_model
        self.orch.minizinc_solver.load_data(self.model_name, minizinc_model, self.task_dzn)

        status, result, warnings = self.orch.minizinc_solver.solve()
        return status, result


    def subroutine_both(self):
        print("subroutine both")

        prompt = self.orch.fetch_control_prompt("both") # ok
        extracted_data, self.messages = self.orch.get_llm_response(prompt.format(input=self.user_input), self.parser_model, self.messages)
        extracted_data = self.extract_task_model(extracted_data)
        if extracted_data:
            self.task = extracted_data["task"]
            self.model = extracted_data["model"]
        return True
    
    def extract_task_model(self, input_string):
        extracted = {}
        try:
            input_string = input_string.split("Model:")
            extracted["model"] = input_string[1]
            if "Task" in input_string[0]: 
                extracted["task"] = input_string[0].split("Task:")[1]
            else:
                extracted["task"] = input_string[0].split("Problem:")[1]
            return extracted
        except Exception as e:
            print(e)
            return False
        
    # TODO what is mode?
    def run_tasks(self, text, experiment_number, models, history, messages, i):
            self.set_models(models)
            status, result = self.start_execution(text, experiment_number, i, messages)
                    
if __name__ == "__main__":

    # Get the value of the OPENAI_API_KEY environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Print the value
    #if openai_api_key:
    #    print("OPENAI_API_KEY is set.")
    #    print(f"Value: {openai_api_key}")
    #else:
    #    print("OPENAI_API_KEY is not set.")

    acmg1 = acmg()

    data = pandas.read_excel("tasks.xlsx", header=None)
    data_array = data.to_numpy()

    p = ai_models.parser()
    r = ai_models.recognizer()
    g = ai_models.generator()
    b = ai_models.base_model()

#              r, g, p, b    ai_models
    models = [[b, b, b, b], 
              [g, g, g, g], 
              [r, g, r, g], 
              [r, g, r, r], 
              [r, g, p, g], 
              [r, g, p, b]]

    history = "_"

    for j in range(len(models)):
            # TODO what is 14
            for i in range(1,14):
                    # TODO what is I do not want to feed it course but some other data?
                    path = f"APLAI_course/{i}/description.txt"
                    with open(path, "r") as file:
                        text = file.read()
                        print(i, text, '\n\n')
                        messages = None

                        # j is the number of the experiment
                        acmg1.run_tasks(text, j, models[j], history, messages, i)






         