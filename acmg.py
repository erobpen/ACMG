
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
from PrettyPrint import PrettyPrintTree
from modules.submodules.recognizer import recognizer
from modules.submodules.generator import generator
from modules.submodules.minizinc_solver import minizinc_solver

def filter_string(input_string):
    pattern = r'[a-zA-Z0-9_]+'
    matches = re.findall(pattern, input_string)
    filtered_string = ''.join(matches)
    return filtered_string

class acmg:

    # logger nek sprema ukupne tokene
    
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
    
    def print_tree(self, x, parrent_id):
        n = node(parrent_id + "0", x, None, [])
        self.tree.add_nodes_to_tree(self.tree, parrent_id, [n])
        PrettyPrintTree(lambda x: x.branches, lambda x: x.task)(self.tree)
        print("\n\n")
    
    def start_execution(self, text, index):

        self.messages = None
        self.task = None
        self.task_dzn = None
        self.model = None

        # self.user_input = self.pc.get_user_prompt()
        self.user_input = text
        prompt = self.pc.fetch_data("assess_user_input")

        provided, self.messages = self.pc.get_llm_response(prompt.format(input=self.user_input), self.parser_model, self.messages)
        print(provided, " is provided,")

        provided = "Both"
        if provided == 'Task':
            # zatrazi model
            self.task = self.user_input
            print("Enter the problem rules:")
            self.model = self.pc.get_user_prompt()
        elif (provided == 'Model'):
            # zatrazi task
            self.model = self.user_input
            print("Enter the problem input information:")
            self.model = self.pc.get_user_prompt()
        elif provided == 'Both':
            self.subroutine_both()
        elif provided == 'None':
            return False
        
        prompt_generate = self.pc.fetch_data("generate")
        subsequent_prompt = self.pc.fetch_data("generate_again") # ok
        prompt_recognize = self.pc.fetch_data("recognize").format(input=self.model)
        prompt_reformat = self.pc.fetch_data("RFS_new")

        # naming of the model

        stored_models = self.pc.fetch_data("stored_models")
        text = "\n".join([key for key in stored_models.keys()])
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
            print("Reformated task: ", self.task_dzn)

        else:
            # model does not exist and needs to be created, task formatting is created based on the minizinc model
            self.model_name, self.messages = self.pc.get_llm_response(self.pc.fetch_data("name_model").format(input=self.model), self.base_model, self.messages)
            status = False

            for i in range(3):
                recognized, self.messages = self.pc.get_llm_response(prompt_recognize, self.recognizer_model, self.messages)
                prompt = prompt_generate.format(model=self.model, recognized=recognized)
                result = None

                # generate (3 attempts)
                for j in range(3):
                    print("=========================================================================")
                    prompt = self.pc.generator.add_warnings(prompt, subsequent_prompt, self.model, recognized, result)
                    mini_zinc_model, self.messages = self.pc.get_llm_response(prompt, self.generator_model, self.messages)
                    print(prompt)

                    # reformat data.dzn
                    self.task_dzn, self.messages = self.pc.get_llm_response(prompt_reformat.format(model=mini_zinc_model, input=self.task), self.generator_model, self.messages)
                    self.pc.mem.store_new_format(self.model_name + "_RFS", self.task)

                    # evaluate
                    status, result = self.pc.minizinc_solver.evaluate(mini_zinc_model, self.model_name, self.task_dzn)
                    print("\n\nminizinc model:\n", mini_zinc_model)
                    print("valid: ", status)
                    print(f"Warnings: \n{result}")
                    if status:
                        with open(str(index + 1) + ".txt", "a") as file2:
                            file2.write(mini_zinc_model)
                            file2.write("\n\n")
                            file2.write(self.task_dzn)

                        with open("res.txt", "a") as file2:
                            try:
                                file2.write(f"{index + 1}: correct: {self.model_name} --- {result}\n")
                            except Exception as e:
                                try:
                                    file2.write(f"{index + 1}: correct: {self.model_name} --- {"".join(list(result)[:7])}")
                                except Exception as e:
                                    file2.write(f"{index + 1}: correct: {self.model_name} --- {result.status}")
                    print("written to res")
                    if status and result.status != 'UNSATISFIABLE':
                        print("Satisfiable: ", result.status)
                        self.pc.mem.store_new_model(self.model_name, mini_zinc_model)
                        break
                    # n = input(">>>>> ")

                if status:
                    break
            

        
        #5 model look up

        # minizinc_model = self.pc.fetch_model(self.model_name)
        minizinc_model = mini_zinc_model
        self.pc.minizinc_solver.load_data(self.model_name, minizinc_model, self.task_dzn)

        # 6 assign
        # napraviti da se vrati assignemnt response koji zahtijeva sto manje formatiranja (da se samo popune vrijednosti, gdje je moguce)
        # prompt = self.pc.fetch_data("assign")
        # assignment, self.messages = self.pc.get_llm_response(prompt, self.base_model, self.messages)

        # 7 solve
        
        status, result = self.pc.minizinc_solver.solve()
        return status, result


    def subroutine_both(self):
        print("subroutine both")

        # popraviti both prompt, trenutno vraca hardcoded response
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
        


if __name__ == "__main__":

    mem1 = mem()
    acmg1 = acmg()


    T = 3
    # acmg1.start_execution()

    results = []
    data = pandas.read_excel("tasks.xlsx", header=None)
    data_array = data.to_numpy()
    print(data_array.shape)

    for i in range(10):
        
        text = data_array[i][0]
        status, result = acmg1.start_execution(text, i)
        try:
            results.append({"task" : i, "status" : status, "solutions" : str(result.solution)})
        except Exception as e:
            results.append({"task" : i, "status" : status, "solutions" : "None"})   
    
        with open("results.txt", "w") as file:
            json.dump(results, file)


