from minizinc import Instance, Model, Solver
import json

def solve():
    try:
        path = "zz_minizinc.mzn"
        model = Model(path)
        
        # Load the data file
        model.add_file("zz_data.dzn")
        
        # Get the Gecode solver
        gecode = Solver.lookup("gecode")
        
        # Create instance
        instance = Instance(gecode, model)
        
        # Don't set n here since it's already defined in the .mzn file
        # instance["n"] = 4  # Remove this line
        
        result = instance.solve()
        
        print("Status:", result.status)
        print("Solution:", result.solution)
        print("Statistics:", result.statistics)
        return True, result
    
    except Exception as e:
        print("Exception occurred:", str(e))
        return False, e

if __name__ == "__main__":
    status, result = solve()