
from minizinc import Instance, Model, Solver
import json


class minizinc_solver:

    def __init__(self):
        self.model_data = None
        self.path = None
        pass

    def load_data(self, model_id, minizinc_model, task):

        # napraviti da se data loada u data.dz file
        # i iskoristava pri solving-u
        # provjeriti flow ako se uvijek radi classify

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

            file.write(minizinc_model)
        
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
        with open(self.path, "w") as file:
            model = model.split("output")[0]
            model = model.replace("\\n", '\n')  
            model = model.replace("```minizinc", "")
            model = model.replace("```", "")
            file.write(model)

        with open("zz_data.dzn", "w") as file:
            task_dzn = task_dzn.replace("\\n", '\n')  

            task_dzn = task_dzn.replace("```dzn", "")
            task_dzn = task_dzn.replace("```", "")

            file.write(task_dzn)
        
        status, result = self.solve()
        return status, result
    
    def print_file(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                print(data)
        except Exception as e:
            print(e)

    def solve(self):
        try:

                    
            model = Model(self.path)

            model.add_file("zz_data.dzn")
            # trenutno je postavljen defaultni gecode solver
            gecode = Solver.lookup("gecode")

            instance = Instance(gecode, model)

            instance["n"] = 4
            result = instance.solve()

            print("status: ", result.status)
            print("solution: ", result.solution)
            print("statistics: ", result.statistics)
            return True, result
        except Exception as e:
            print("Exception occured")
            return False, e
