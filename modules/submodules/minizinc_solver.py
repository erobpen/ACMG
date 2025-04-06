
from minizinc import Instance, Model, Solver
import json



def clean_text_for_writing(text, error):
    """
    Removes characters that cause UnicodeEncodeError in Windows charmap codec.
    
    Args:
        text (str): The original text to clean
        error (Exception): The UnicodeEncodeError exception
        
    Returns:
        str: Text with problematic characters removed
    """
    if not isinstance(error, UnicodeEncodeError):
        return text
        
    # Extract position information from the error message
    try:
        # Parse error positions from the error message
        error_msg = str(error)
        start_pos = int(error_msg.split('position ')[1].split('-')[0])
        end_pos = int(error_msg.split('-')[1].split(':')[0])
        
        # Create a new string excluding the problematic range
        cleaned_text = text[:start_pos] + text[end_pos + 1:]
        return cleaned_text
        
    except (ValueError, IndexError):
        # If we can't parse the error message, remove all non-ASCII characters
        return ''.join(char for char in text if ord(char) < 128)
    

class minizinc_solver:

    def __init__(self):
        self.model_data = None
        self.path = None
        #TODO remove pass
        pass

    def load_data(self, model_id, minizinc_model, task):


        # self.path = model_id + ".mzn"
        self.path = "zz_minizinc.mzn"
        with open(self.path, "w") as file:
            minizinc_model = minizinc_model.replace("AXa", "\n")
            minizinc_model = minizinc_model.replace("XXx", "\\")
            minizinc_model = minizinc_model.replace("'", '"')

            minizinc_model = minizinc_model.split("output")[0]
            minizinc_model = minizinc_model.replace("\\n", '\n') 

            minizinc_model = minizinc_model.replace("```minizinc", "")
            minizinc_model = minizinc_model.replace("```", "")
            try:
                file.write(minizinc_model)
            except Exception as e:
                try:
                    file.write(clean_text_for_writing(minizinc_model, e))
                except Exception as e:
                    pass
        
        with open("zz_data.dzn", "w") as file:

            task = task.replace("```dzn", "")
            task = task.replace("```", "")

            file.write(task)

        self.model_data = minizinc_model
        self.task = task
        return True
    
    
    def evaluate(self, model, model_name, task_dzn):
        # self.path = model_name + ".mzn"
        self.path = "zz_minizinc.mzn"
        with open(self.path, "wb") as file:
            model = model.split("output")[0]
            model = model.replace("\\n", '\n')  
            model = model.replace("```minizinc", "")
            model = model.replace("```", "")
            model = 'include "alldifferent.mzn";\n\n' + model
            try:
                file.write(model.encode("utf-8"))
            except Exception as e:
                pass

        with open("zz_data.dzn", "wb") as file:
            task_dzn = task_dzn.replace("\\n", '\n')  

            task_dzn = task_dzn.replace("```dzn", "")
            task_dzn = task_dzn.replace("```", "")

            try:
                file.write(task_dzn.encode("utf-8"))
            except Exception as e:
                pass
        
        status, result, warnings = self.solve()
        return status, result, warnings
    
    def print_file(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                print(data)
        except Exception as e:
            print(e)

    def solve(self):

        result = None
        result_2 = None
        warnings = None

        try:
            self.path = "zz_minizinc.mzn"
            model = Model(self.path)

            model.add_file("zz_data.dzn")

            # default solver is set to gecode
            gecode = Solver.lookup("gecode")

            instance = Instance(gecode, model)

            instance["n"] = 4
            result = instance.solve()
            # print("status: ", result.status)
            # print("solution: ", result.solution)
            # print("statistics: ", result.statistics)
        except Exception as e:
            # print("Warnings for result 1: ", e)
            warnings = e

        try:
            self.path = "zz_minizinc.mzn"
            model = Model(self.path)
            gecode = Solver.lookup("gecode")
            instance = Instance(gecode, model)
            instance["n"] = 4
            result_2 = instance.solve()



            # print("status: ", result.status)
            # print("solution: ", result.solution)
            # print("statistics: ", result.statistics)
        except Exception as e:
            pass
            # print("Warnings for result 2: ", e)
            
        print("RESULT_1: ", result)
        print("RESULT_2: ", result_2)
        result = result_2 if result_2 != None else result
        if result:
            print("Choosing result 1")
        
        return True, result, warnings