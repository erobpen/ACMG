
import sys
import os, time, re, pandas, json
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path1 = dir_path + '\\models'
dir_path2 = dir_path + '\\modules'
sys.path.insert(0, dir_path1)
sys.path.insert(0, dir_path2)   
from modules import ai_models
from modules.pc import pc 
from modules.mem import mem
from modules.submodules.tree import node
from modules.submodules.recognizer import recognizer
from modules.submodules.generator import generator
from modules.submodules.minizinc_solver import minizinc_solver

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

        self.pc = pc(minizinc_solver1, recognizer1, generator1, self.mem)
        self.user_input = None
        self.task = None
        self.task_dzn = None
        self.model = None
        self.model_name = None
        self.messages = None
        pass

    def set_models(self, models):
        self.recognizer_model = models[0]
        self.generator_model = models[1]
        self.parser_model = models[2]
        self.base_model = models[3]
    
    def print_tree(self, x, parrent_id):
        n = node(parrent_id + "0", x, None, [])
        self.tree.add_nodes_to_tree(self.tree, parrent_id, [n])
        PrettyPrintTree(lambda x: x.branches, lambda x: x.task)(self.tree)
        print("\n\n")
    
    def start_execution(self, text, mode, index, messages):

        self.messages = messages
        self.task = None
        self.task_dzn = None
        self.model = None

        # self.user_input = self.pc.get_user_prompt()
        self.user_input = text
        # prompt should be called control_prompt
        prompt = self.pc.fetch_data("assess_user_input")

        provided, self.messages = self.pc.get_llm_response(prompt.format(input=self.user_input), self.parser_model, self.messages)
        print("Provided: \n", provided)

        # provided = "Both"
        if provided == 'Task':
            # zatrazi model
            self.task = self.user_input
            print("Enter the problem rules:")
            # self.model = self.pc.get_user_prompt()
            self.model = self.user_input
        elif (provided == 'Model'):
            # zatrazi task
            self.model = self.user_input
            print("Enter the problem input information:")
            # self.task = self.pc.get_user_prompt()
            self.task = self.user_input
        elif provided == 'Both':
            self.subroutine_both()
        elif 'None' in provided or 'none' in provided:
            # return False
            self.task = self.user_input
            self.model = self.user_input
            self.subroutine_both()

        
        prompt_generate = self.pc.fetch_data("generate")
        subsequent_prompt = self.pc.fetch_data("generate_again") # ok
        prompt_recognize = self.pc.fetch_data("recognize").format(input=self.model)
        #TODO rename RFS into Input prepration poin 7 in figure short version IP
        prompt_reformat = self.pc.fetch_data("RFS_new")

        # naming of the model

        stored_models = self.pc.fetch_data("stored_models")
        text = "\n".join([key for key in stored_models.keys()])
        #TODO remove or comment out CFS and all relate to CFS
        prompt = self.pc.fetch_data("CFS")
        classification, self.messages = self.pc.get_llm_response(prompt.format(stored_models=text, input=self.user_input), self.recognizer_model, self.messages)
        classification = "false"

        # ovo bi trebao biti model name
        print("Already existing: ", classification)

        if ('false' not in classification and 'False' not in classification):
            # model exists and can be used as well as the task format
            self.model_name = classification
            
            prompt = self.pc.fetch_data(self.model_name + "_RFS")
            self.task_dzn, self.messages = self.pc.get_llm_response(prompt.format(input=self.task), self.base_model, self.messages)
            # print("Reformated task: ", self.task_dzn)

        else:
            # model does not exist and needs to be created, task formatting is created based on the minizinc model
            self.model_name, self.messages = self.pc.get_llm_response(self.pc.fetch_data("name_model").format(input=self.model), self.base_model, self.messages)
            status = False
            results = []
            minizinc_models = ""
            warnings = None

            for i in range(3):
                recognized, self.messages = self.pc.get_llm_response(prompt_recognize, self.recognizer_model, self.messages)
                #TODO control prompt
                prompt = prompt_generate.format(model=self.model, recognized=recognized)
                result = None
                warnings = None

                # generate (3 attempts)
                for j in range(3):
                    # print("=========================================================================")
                    print("Warnings for attempt " + str(j + 1) + ": ", warnings)
                    prompt = self.pc.generator.add_warnings(prompt, subsequent_prompt, self.model, recognized, warnings)
                    mini_zinc_model, self.messages = self.pc.get_llm_response(prompt, self.generator_model, self.messages)
                    # print(prompt)

                    #TODO reformat i.e. IP should be done after we get valid MiniZinc model when syntax in verified with MiniZinc solver, move this code on right place
                    # reformat data.dzn
                    self.task_dzn, self.messages = self.pc.get_llm_response(prompt_reformat.format(model=mini_zinc_model, input=self.task), self.generator_model, self.messages)
                    self.pc.mem.store_new_format(self.model_name + "_RFS", self.task)

                    # evaluate
                    status, result, warnings = self.pc.minizinc_solver.evaluate(mini_zinc_model, self.model_name, self.task_dzn)
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

                    # provjeri ove uvjete jel se ispunjavaju dobro 
                    if (result != None):
                        print("Satisfiable: ", result.status)
                    if (result != None) and (str(result.status) == 'SATISFIED'):
                        self.pc.mem.store_new_model(self.model_name, mini_zinc_model)
                        break
                    # n = input(">>>>> ")
                
                if (result != None) and (str(result.status) == 'SATISFIED'):
                    print("CONDITION MET")
                    break
            print("-" * 50)
            print("FILENAME: " + "rezultati\\" + history + "_" + "experiment_" + str(mode) +"_problem_" + str(index) +  ".txt")
            print("-" * 50)
            with open("rezultati\\" + history + "_" + "experiment_" + str(mode) +"_problem_" + str(index) +  ".txt", "w") as file:
                json.dump(results, file)
                
                if results == []:
                    print("No results\n")
            with open("rezultati\\" + history + "_" + "experiment_" + str(mode) +"_problem_" + str(index) +  ".txt", "a") as file:
                file.write("\n\n")
                file.write(minizinc_models)
            

        
        #5 model look up

        # minizinc_model = self.pc.fetch_model(self.model_name)
        minizinc_model = mini_zinc_model
        self.pc.minizinc_solver.load_data(self.model_name, minizinc_model, self.task_dzn)

        # 6 assign
        # assignment is done in the sequential minizinc code generation attempts

        # 7 solve
        
        status, result, warnings = self.pc.minizinc_solver.solve()
        return status, result


    def subroutine_both(self):
        print("subroutine both")

        prompt = self.pc.fetch_data("both") # ok
        extracted_data, self.messages = self.pc.get_llm_response(prompt.format(input=self.user_input), self.parser_model, self.messages)
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
        

    def run_tasks(self, text, mode, models, history, messages, i):
            
            self.set_models(models)
            status, result = self.start_execution(text, mode, i, messages)
                    
if __name__ == "__main__":

    # Get the value of the OPENAI_API_KEY environment variable
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Print the value
    if openai_api_key:
        print("OPENAI_API_KEY is set.")
        print(f"Value: {openai_api_key}")
    else:
        print("OPENAI_API_KEY is not set.")
    
    mem1 = mem()
    acmg1 = acmg()


    T = 3

    data = pandas.read_excel("tasks.xlsx", header=None)
    data_array = data.to_numpy()

    p = ai_models.parser()
    r = ai_models.recognizer()
    g = ai_models.generator()
    b = ai_models.base_model()


        #      r, g, p, b    ai_models
    models = [[b, b, b, b], 
             [g, g, g, g], 
             [r, g, r, g], 
             [r, g, r, r], 
             [r, g, p, g], 
             [r, g, p, b]]


    history = "_"


    for j in range(len(models)):

            for i in range(1,14):
                #TODO remove debuging code
                if j == 1 and i <= 9:
                    continue
                else:
                    path = f"APLAI_course/{i}/description.txt"
                    with open(path, "r") as file:
                        text = file.read()
                        print(i, text, '\n\n')
                        messages = None
                        acmg1.run_tasks(text, j, models[j], history, messages, i)






         