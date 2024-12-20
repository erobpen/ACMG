import json
from minizinc import Instance, Model, Solver

class mem:

    def __init__(self):
        self.datapath = "./data.json"

        # print("mc initialised")
    
    def return_data(self, prompt_id):
        file = open(self.datapath, "r")
        data = json.load(file)
        file.close()
        return data[prompt_id]

    def store_end_results(self, result: dict, task_id) -> bool:
        with open(self.datapath, "r") as file:
            try:
                data = json.load(file)

                data["results"][task_id].append(result)
                with open(self.datapath, "w") as file:
                    json.dump(data, file)
                return True
            except Exception as e:
                print(e)
                return False
    
    def store_progress(self, tree: dict) -> bool:
        try:
            with open(self.datapath, "r") as file:
                data = json.load(file)
                data["progress_tree"] = tree
                with open(self.datapath, "w") as file:
                    json.dump(data, file)
                return True
        except Exception as e:
            print(e)
            return False
        
    def store_new_model(self, model_id, text) -> bool:
        try:
            with open(self.datapath, "r") as file:
                data = json.load(file)
                text = text.replace('\\', "XXx")
                text = text.replace('"', "'")
                data["stored_models"][model_id] = text
                with open(self.datapath, "w") as file:
                    json.dump(data, file)
            return True
        except Exception as e:
            print(e)
            return False
        
    def store_new_format(self, format_id, text) -> bool:
        try:
            with open(self.datapath, "r") as file:
                data = json.load(file)
                data[format_id] = text
                with open(self.datapath, "w") as file:
                    json.dump(data, file)
                return True
        except Exception as e:
            print(e)
            return False
        
    def print_file(self, path):
        try:
            with open(path, "r") as file:
                data = json.load(file)
                print(data)
        except Exception as e:
            print(e)

    def run_model(self , model_id):
        try:
            data = self.return_data(model_id)
            path = model_id + ".mzn"
            with open(path, "w") as file:
                file.write(data)
            model = Model(path)

            # trenutno je postavljen defaultni gecode solver
            gecode = Solver.lookup("gecode")

            instance = Instance(gecode, model)

            instance["n"] = 4
            result = instance.solve()

            print(result, "\n\n")
        except Exception as e:
            print(e)
        