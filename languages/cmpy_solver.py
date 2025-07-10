
import cpmpy as cp
import subprocess



class CMPySolver:
    def __init__(self, model):
        self.model = model

    def solve(self):
        # Create a solver instance
        solver = cp.Model(self.model)

        # Solve the model
        if solver.solve():
            return True, solver.value()
        else:
            return False, None

    def get_solution(self):
        # Get the solution from the last solve attempt
        return self.model.value() if self.model.is_solved() else None
    
    def evaluate(self, model, model_name, task_dzn):

        with open("model.py", "w") as f:
            f.write(model)

            try:
                result = subprocess.run(
                    ["python", "model.py"],
                    capture_output=True,
                    text=True
                )
                outputs = result.stdout + result.stderr
            except Exception as e:
                outputs = str(e)

            with open("solution_cpy.py", "r") as f:
                result = f.read()
                
            warnings = outputs
            status = "dohvati solve output, true ili false"
            return status, result, warnings





