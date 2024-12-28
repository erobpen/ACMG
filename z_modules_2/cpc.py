
import sys
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '..')

from modules.mem import mem
from submodules.prunner import prunner
from submodules.aggregator import aggregator
from submodules.generator import generator
from submodules.dsc import dsc

class cpc:

    def __init__(self):
        self.prunner = None
        self.generator = None
        self.aggregator = None
        self.validate = None
        self.get_solutions = None
        self.dsc = dsc()
        # print("cpc initialised")

    def fetch_data(self, prompt_id, mc : mc) -> dict:
        return mc.return_data(prompt_id)

    def format_prompt(self, prompt: str, pm=None, task_input=None) -> str:
        return prompt.format(pm=pm, task_input=task_input)

    def update_rt(self, rt: dict) -> dict:
        pass

    def separate(self, all_solutions, initial_task):
        solutions = []
        no_goods = []
        for solution in all_solutions:
            if self.validate(solution, initial_task):
                solutions.append(solution)
            else:
                no_goods.append(solution)
        return solutions, no_goods
        



if __name__ == "__main__":

    print("hello")

    


