
import re, os, sys, random
from   itertools  import permutations, combinations, product, \
                         chain
import math as m
from itertools import zip_longest
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '..')
from modules.submodules.prunner import prunner
from modules.submodules.generator import generator
from modules.submodules.aggregator import aggregator
from fractions import Fraction as F


class dsc:

    def __init__(self):
        self.check_constraints = None
        self.set_domains = None
        self.extract_solutions = None
        self.set_args = None
        self.format_prompt = None
        self.set_initial_domains_and_args = None
        self.validator = None
        self.args = {}
        pass

    def cross(self, A, B):
        return [a+b for a in A for b in B]
    
    def clean(self, string_list):
        lista = re.sub(r'[()* / +|—,.-]+', '', string_list)
        return lista
    
    def clean_prompt(self, puzzle_solution):

        try:
            puzzle_solution = puzzle_solution.split('\n')
            array = []
            for i in range(len(puzzle_solution)):
                if "|" in puzzle_solution[i]:
                    array.append(puzzle_solution[i])
                if "END" in puzzle_solution[i]:
                    break

            array.remove(array[0])
            array = [x.strip() for x in array]
            for line in array:
                if '-' in line:
                    array.remove(line)
            for i in range(len(array)):
                array[i] = array[i].strip("|")
            lines = []
            for line in array:
                line = line.split("|")
                lines.append(line)
            string = ""
            for i in range(len(lines)):
                for j in range(len(lines[i])):
                    if "   " in lines[i][j]:   
                        string += '0'
                    else:
                        string += lines[i][j].strip()
            return string
        except Exception as e:
            print(e)
            return False
    
    def solve(self, digits):
        solutions = []
        digilen = len(digits)
        exprlen = 2 * digilen - 1
        digiperm = sorted(set(permutations(digits)))
        opcomb   = list(product('+-*/', repeat=digilen-1))
        brackets = ( [()] + [(x,y)
                            for x in range(0, exprlen, 2)
                            for y in range(x+4, exprlen+2, 2)
                            if (x,y) != (0,exprlen+1)]
                    + [(0, 3+1, 4+2, 7+3)] )
        for d in digiperm:
            for ops in opcomb:
                if '/' in ops:
                    d2 = [('F(%s)' % i) for i in d]
                else:
                    d2 = d
                ex = list(chain.from_iterable(zip_longest(d2, ops, fillvalue='')))
                for b in brackets:
                    exp = ex[::]
                    for insertpoint, bracket in zip(b, '()'*(len(b)//2)):
                        exp.insert(insertpoint, bracket)
                    txt = ''.join(exp)
                    try:
                        num = eval(txt)
                    except ZeroDivisionError:
                        continue
                    if num == 24:
                        if '/' in ops:
                            exp = [ (term if not term.startswith('F(') else term[2:-1])
                                for term in exp ]
                        ans = ' '.join(exp).rstrip()
                        ans = "".join(ans.split(" "))
                        solutions.append(ans)
                        continue        
        return solutions
    
    def check_constraints_sudoku(self, args, first_node, second_node, v, w):
        if v == w: 
            return False
        return True

    def check_constraints_g24(self, args, first_node, second_node, v, w):

        expression = args['new_values'][list(args['new_values'].keys())[0]]
        if expression == False: return False
        step = args['step']
        solutions = args['solutions']
        satisfies_with_some = False
        if (step == 1) & (len(expression) >= 5):
            if first_node == 'A3':
                for solution in solutions:
                    whole_expression1 = '(' + w +')' +  v
                    whole_expression2 = v + '(' + w +')'
                    if (whole_expression1 in solution) | (whole_expression2 in solution):
                        satisfies_with_some = True
                        break


            if second_node == 'A3':
                for solution in solutions:
                        whole_expression1 = '(' + v +')' +  w
                        whole_expression2 = w + '(' + v +')'
                        if (whole_expression1 in solution) | (whole_expression2 in solution):
                            satisfies_with_some = True
                            break
        else:
            for solution in solutions:
                if (v in solution) & (w in solution):
                    satisfies_with_some = True
                    break
        return satisfies_with_some

    def set_initial_domains_and_args_g24(self, task_input):
        numbers = task_input.strip().split(' ')
        values = {'A1': '','A2': '','A3': '', 'remaining': numbers}
        queue = ['A2A1', 'A1A3', 'A3A1', 'A2A3', 'A3A2', 'A1A2']
        self.args['queue'] = queue
        self.args['solutions'] = self.solve(numbers)
        self.args['numbers'] = numbers
        self.args['variables'] = ['A1', 'A2', 'A3']
        return values
    
    def set_initial_domains_and_args_sudoku_9(self, task_input, prunner : prunner):
        
        values = {'A1': '', 'A2' : '', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'A7': '', 'A8': '', 'A9': '', 'B1': '', 'B2': '', 'B3': '', 'B4': '', 'B5': '', 'B6': '', 'B7': '', 'B8': '', 'B9': '', 'C1': '', 'C2': '', 'C3': '', 'C4': '', 'C5': '', 'C6': '', 'C7': '', 'C8': '', 'C9': '', 'D1': '', 'D2': '', 'D3': '', 'D4': '', 'D5': '', 'D6': '', 'D7': '', 'D8': '', 'D9': '', 'E1': '', 'E2': '', 'E3': '', 'E4': '', 'E5': '', 'E6': '', 'E7': '', 'E8': '', 'E9': '', 'F1': '', 'F2': '', 'F3': '', 'F4': '', 'F5': '', 'F6': '', 'F7': '', 'F8': '', 'F9': '', 'G1': '', 'G2': '', 'G3': '', 'G4': '', 'G5': '', 'G6': '', 'G7': '', 'G8': '', 'G9': '', 'H1': '', 'H2': '', 'H3': '', 'H4': '', 'H5': '', 'H6': '', 'H7': '', 'H8': '', 'H9': '', 'I1': '', 'I2': '', 'I3': '', 'I4': '', 'I5': '', 'I6': '', 'I7': '', 'I8': '', 'I9': ''}
        for key in values:
            values[key] = list("123456789")
            
        self.args["new_values"] = self.get_new_assignments_sudoku_9(task_input, values)
        values = prunner.assign(values, self.args)
        return values
    
    def set_initial_domains_and_args_sudoku_9(self, task_input, prunner : prunner):
        
        values = {'A1': '', 'A2' : '', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'A7': '', 'A8': '', 'A9': '', 'B1': '', 'B2': '', 'B3': '', 'B4': '', 'B5': '', 'B6': '', 'B7': '', 'B8': '', 'B9': '', 'C1': '', 'C2': '', 'C3': '', 'C4': '', 'C5': '', 'C6': '', 'C7': '', 'C8': '', 'C9': '', 'D1': '', 'D2': '', 'D3': '', 'D4': '', 'D5': '', 'D6': '', 'D7': '', 'D8': '', 'D9': '', 'E1': '', 'E2': '', 'E3': '', 'E4': '', 'E5': '', 'E6': '', 'E7': '', 'E8': '', 'E9': '', 'F1': '', 'F2': '', 'F3': '', 'F4': '', 'F5': '', 'F6': '', 'F7': '', 'F8': '', 'F9': '', 'G1': '', 'G2': '', 'G3': '', 'G4': '', 'G5': '', 'G6': '', 'G7': '', 'G8': '', 'G9': '', 'H1': '', 'H2': '', 'H3': '', 'H4': '', 'H5': '', 'H6': '', 'H7': '', 'H8': '', 'H9': '', 'I1': '', 'I2': '', 'I3': '', 'I4': '', 'I5': '', 'I6': '', 'I7': '', 'I8': '', 'I9': ''}
        for key in values:
            values[key] = list("123456789")

            
        self.args["new_values"] = self.get_new_assignments_sudoku_9(task_input, values)
        values = prunner.assign(values, self.args)
        return values
    
    def set_initial_domains_and_args_sudoku_6(self, task_input, prunner : prunner):
        
        values = {'A1': '', 'A2': '', 'A3': '', 'A4': '', 'A5': '', 'A6': '', 'B1': '', 'B2': '', 'B3': '', 'B4': '', 'B5': '', 'B6': '', 'C1': '', 'C2': '', 'C3': '', 'C4': '', 'C5': '', 'C6': '', 'D1': '', 'D2': '', 'D3': '', 'D4': '', 'D5': '', 'D6': '', 'E1': '', 'E2': '', 'E3': '', 'E4': '', 'E5': '', 'E6': '', 'F1': '', 'F2': '', 'F3': '', 'F4': '', 'F5': '', 'F6': ''}
        for key in values:
            values[key] = list("123456")

            
        self.args["new_values"] = self.get_new_assignments_sudoku_6(task_input, values)
        for key in self.args["new_values"]:
            values[key] = self.args["new_values"][key]
        return values
    
    def set_initial_domains_and_args_sudoku_4(self, task_input, prunner : prunner):
        
            values = {'A1': '', 'A2': '', 'A3': '', 'A4': '', 'B1': '', 'B2': '', 'B3': '', 'B4': '', 'C1': '', 'C2': '', 'C3': '', 'C4': '', 'D1': '', 'D2': '', 'D3': '', 'D4': ''}
            for key in values:
                values[key] = list("1234")

                
            self.args["new_values"] = self.get_new_assignments_sudoku_6(task_input, values)
            for key in self.args["new_values"]:
                values[key] = self.args["new_values"][key]
            return values
        
    


    def queue_init(self, peers):
        queue = []
        for key in peers:
            for peer in peers[key]:
                arc = str(key) + str(peer)
                queue.append(arc)
        random.shuffle(queue)
        return queue

    def set_domains_sudoku_9(self, values):
        for key in values:
            values[key] = list("123456789")
        for variable in self.args["new_values"]:
            values[variable] = self.args["new_values"][variable]
        return True, values
    
    def set_domains_sudoku_6(self, values):
        for key in values:
            values[key] = list("123456")
        for variable in self.args["new_values"]:
            values[variable] = self.args["new_values"][variable]
        return True, values
    
    def set_domains_sudoku_4(self, values):
        for key in values:
            values[key] = list("1234")
        for variable in self.args["new_values"]:
            values[variable] = self.args["new_values"][variable]
        return True, values


    def set_domains_g24(self, values):

        numbers = self.args["numbers"]
        step = self.args["step"]
        new_values = self.args["new_values"]
        expression = new_values[list(new_values.keys())[0]]

        try:
            if step == 0:

                initial_domain = numbers.copy()
                values = {'A1': '','A2': '','A3': ''}
                operators = '+-*/'
                first_number = expression.split(' ')[0]
                second_number = expression.split(' ')[2]
                try:
                    initial_domain.remove(first_number)
                    initial_domain.remove(second_number)
                    values['remaining'] = initial_domain
                except Exception as e:
                    #print(e)
                    return False, False
                first = [first_number, second_number]
                remaining = [x for x in numbers if x not in first]
                combinations = self.cross(remaining, operators)
                combinations.extend(self.cross(operators, remaining))
                values['A2'] = combinations.copy()
                values['A3'] = combinations.copy()
                values['A1'] = ["".join(expression.split(' '))]

            elif step == 1:
                values['A2'] = ["".join(expression.split(' '))]
                if len(expression) >= 5:
                        first = expression.split(' ')[0]
                        second = expression.split(' ')[2]
                        if (first not in values['remaining']) | (second not in values['remaining']):
                            return False, False
                        values['A3'] = ['+','-','*','/']
                else:
                    second = self.clean(expression)
                    remaining = values['remaining'].copy()
                    remaining.remove(second)
                    operators = '+-*/'
                    combinations = self.cross(remaining, operators)
                    combinations.extend(self.cross(operators, remaining))
                    values['A3'] = combinations
            return True, values
        except Exception as e:
            return False, False
    
    def get_new_assignments_sudoku_9(self, puzzle, values):

        assigned_variables = {}
        try:
            puzzle = self.clean_prompt(puzzle)
            if puzzle == False:
                return False
            digits = '123456789'
            chars = [c for c in puzzle if c in digits or c in '0.']
            filled = dict(zip(self.args['variables'], chars))

            for key in filled:
                if (filled[key] == '0') | (filled[key] == '.'):
                    continue
                else:
                    if (len(values[key]) == 1) & (filled[key] != values[key][0]):
                        return False
                    assigned_variables[key] = list(str(filled[key]))
        except Exception as e:
            print(e)
        return assigned_variables
    
    def get_new_assignments_sudoku_6(self, puzzle, values):

        assigned_variables = {}
        try:
            puzzle = self.clean_prompt(puzzle)
            if puzzle == False:
                return False
            digits = '123456'
            chars = [c for c in puzzle if c in digits or c in '0.']
            filled = dict(zip(self.args['variables'], chars))

            for key in filled:
                if (filled[key] == '0') | (filled[key] == '.'):
                    continue
                else:
                    if (len(values[key]) == 1) & (filled[key] != values[key][0]):
                        return False
                    assigned_variables[key] = list(str(filled[key]))
        except Exception as e:
            print(e)
        return assigned_variables
    
    def get_new_assignments_sudoku_4(self, puzzle, values):

        assigned_variables = {}
        try:
            puzzle = self.clean_prompt(puzzle)
            if puzzle == False:
                return False
            digits = '1234'
            chars = [c for c in puzzle if c in digits or c in '0.']
            filled = dict(zip(self.args['variables'], chars))

            for key in filled:
                if (filled[key] == '0') | (filled[key] == '.'):
                    continue
                else:
                    if (len(values[key]) == 1) & (filled[key] != values[key][0]):
                        return False
                    assigned_variables[key] = list(str(filled[key]))
        except Exception as e:
            print(e)
        return assigned_variables
        

    def get_new_values_g24(self, expression, y):

        numbers = y.domains['remaining']
        if expression == '': return False
        expression = expression.split("\n")
        expression = [e for e in expression if e]

        try:
            if (len(expression) == 1) & ('=' in expression[0]):
                expression = [y.task, expression[0]]
            first_and_second = expression[1].split('=')[0].strip().split(' ')
            first = first_and_second[0]
            second = first_and_second[-1]
            if (first in numbers) & (second in numbers):
                result = expression[1].split('=')[0].strip()
                return result
            else:
                second_expression = expression[1].split('=')[0]
                first = ((((expression[0]).split('('))[0]).split('='))[1].strip()
                left = "".join((expression[0].split("left:")[1]).split(')')).strip().split(' ')
                if len(expression) == 2:
                    
                    second_expression_list = (second_expression.strip().split(' '))
                    if (second_expression_list[0] not in left) & (second_expression_list[2] not in left):
                        return False
                    if (second_expression_list[0] in numbers) & (second_expression_list[2] in numbers):
                        return second_expression
                    if (second_expression_list[0] in numbers) & (second_expression_list[2] not in numbers):
                        result = second_expression_list[0] + second_expression_list[1]
                        result = ("".join(result.split(' '))).strip()
                        return result
                    if (second_expression_list[0] not in numbers) & (second_expression_list[2] in numbers):
                        result = second_expression_list[1] + second_expression_list[2]
                        result = ("".join(result.split(' '))).strip()
                        return result
                    return False
                third_row = expression[2].split('=')[0].strip().split(' ')
                if 'left' not in expression[2]:
                    return False
                if third_row[0] in numbers:
                    return third_row[0] + third_row[1]
                elif third_row[2] in numbers:
                    return third_row[1] + third_row[2]
                else:
                    return False
        except Exception as e:
            return False
    
    def extract_solutions_g24(self, net_y_message_list):
        key = list(net_y_message_list[0].keys())[0]
        new_net_y_message_list = []
        solutions = key.split('\n')
        for s in solutions:
            new_net_y_message_list.append({s: net_y_message_list[0][key]})
        return new_net_y_message_list


    def set_args_g24(self, x, y, step):
        new_values = self.get_new_values_g24(y.task + '\n' + x, y)
        self.args["new_values"] = {self.args['variables'][step] : new_values}
        self.args['step'] = step
        self.args['x'] = x
        return True

    def set_args_sudoku_9(self, x, y, step):
        new_assignments = self.get_new_assignments_sudoku_9(x, y.domains.copy())
        if new_assignments == False:
            return False
        self.args["new_values"] = new_assignments
        self.args['step'] = step
        self.args['x'] = x
        return True
    
    def set_args_sudoku_6(self, x, y, step):
        new_assignments = self.get_new_assignments_sudoku_6(x, y.domains.copy())
        if new_assignments == False:
            return False
        self.args["new_values"] = new_assignments
        self.args['step'] = step
        self.args['x'] = x
        return True
    
    def set_args_sudoku_4(self, x, y, step):
        new_assignments = self.get_new_assignments_sudoku_4(x, y.domains.copy())
        if new_assignments == False:
            return False
        self.args["new_values"] = new_assignments
        self.args['step'] = step
        self.args['x'] = x
        return True
    
    
    def get_current_numbers(self, y: str) -> str:
        last_line = y.strip().split('\n')[-1]
        return last_line.split('left: ')[-1].split(')')[0]
    
    
    def format_prompt_g24(self, nefs_prompt, y, branching_strategy) -> str:
        task = y.task
        current_numbers = self.get_current_numbers(task if task else '')
        prompt = nefs_prompt.format(task=current_numbers)
        return prompt
    
    def validate_g24_BFS_AC3(self, response, task_input):

        lines = response.split('\n')
        if '' in lines:
            lines.remove('')
        first_equation = (lines[0].split('='))[0].strip()
        first_equation = round(eval(first_equation), 1)
        
        second_equation = (lines[1].split('='))[0].strip()
        second_equation = round(eval(second_equation), 1)

        third_equation = (lines[2].split('='))[0].strip()

        first_result = (lines[0].split('(left')[0]).split('=')[1]
        first_result = round(float(first_result), 1)

        second_result = (lines[1].split('(left')[0]).split('=')[1]
        second_result = round(float(second_result), 1)
        try:
            if first_equation == first_result:
                if second_equation == second_result:    
                    if eval(third_equation) == 24:
                        return True
        except Exception as e:
            return False
        return False
    
    def format_prompt_sudoku_9(self, nefs_prompt, y, branching_strategy):
        if branching_strategy == "BFS_AC3":
            puzzle_dict = y.domains
        if branching_strategy == "ENUM":
            return nefs_prompt.format(task=y)
        rows = 'ABCDEFGHI'
        cols = '123456789'
        
        grid = "|-----|-----|-----|-----|-----|-----|-----|-----|-----|\n"
        
        for r in rows:
            row_str = "|"
            for c in cols:
                cell = r + c
                if len(puzzle_dict[cell]) == 1:
                    row_str += f"  {puzzle_dict[cell][0]}  |"
                else:
                    row_str += "     |"
            grid += row_str + "\n|-----|-----|-----|-----|-----|-----|-----|-----|-----|\n"
        
        return nefs_prompt.format(task=grid)
    
    def format_prompt_sudoku_6(self, nefs_prompt, y, branching_strategy):
        if branching_strategy == "BFS_AC3":
            puzzle_dict = y.domains
        if branching_strategy == "ENUM":
            return nefs_prompt.format(task=y)
        rows = 'ABCDEF'
        cols = '123456'
        
        grid = "|-----|-----|-----|-----|-----|-----|\n"
        
        for r in rows:
            row_str = "|"
            for c in cols:
                cell = r + c
                if len(puzzle_dict[cell]) == 1:
                    row_str += f"  {puzzle_dict[cell][0]}  |"
                else:
                    row_str += "     |"
            grid += row_str + "\n|-----|-----|-----|-----|-----|-----|\n"
        
        return nefs_prompt.format(task=grid)
    
    def format_prompt_sudoku_4(self, nefs_prompt, y, branching_strategy):
        if branching_strategy == "BFS_AC3":
            puzzle_dict = y.domains
        if branching_strategy == "ENUM":
            return nefs_prompt.format(task=y)
        rows = 'ABCD'
        cols = '1234'
        
        grid = "|-----|-----|-----|-----|\n"
        
        for r in rows:
            row_str = "|"
            for c in cols:
                cell = r + c
                if len(puzzle_dict[cell]) == 1:
                    row_str += f"  {puzzle_dict[cell][0]}  |"
                else:
                    row_str += "     |"
            grid += row_str + "\n|-----|-----|-----|-----|\n"
        
        return nefs_prompt.format(task=grid)
    
    def make_grid(self, flattened: str, size: int, row_mod = 0, col_mod = 0):
        string = ''
        flattened = list(flattened)
        if (size == 9):
            line = "|-----|-----|-----|-----|-----|-----|-----|-----|-----|\n"
        if (size == 6):
            line = "|-----|-----|-----|-----|-----|-----|\n"
        if (size == 4):
            line = "|-----|-----|-----|-----|\n"
        
        for i in range(size + 1):
            string += line
            if i == size:
                break
            string += '|  '
            for j in range(size + 1):
                if (flattened[i * size + j] == '0'):
                    string += ' '
                else:
                    string += flattened[i * size + j].strip()
                string += '  |  '
                if j == size - 1:
                    string += '\n'
                    break
        return string



    def extract_solutions_sudoku(self, net_y_message_list):
        new_net_y_message_list = []
        for net_y_message_pair in net_y_message_list:
            key = list(net_y_message_pair.keys())[0]
            net_message = key.split('END')
            new_net_y_message_list.append({net_message[0] : net_y_message_pair[key]})
        return new_net_y_message_list
    
    def print_node_g24(self, x):
        return x.split('(left')[0].strip()
    
    def print_node_sudoku_9(self, x):
        try:
            x = self.clean_prompt(x)
            if x == False:
                return "Not printable"
            x = list(x)
            node_text = ""
            for i in range(9):
                for j in range(9):
                    if x[i * 9 + j] != '0':
                        node_text += x[i * 9 + j]
                    else:
                        node_text += '.'
                node_text += '\n'
            return node_text + f"   [{81 - node_text.count('.')}]   "
        except Exception as e:
            return "Not printable"
        
    def print_node_sudoku_6(self, x):
        try:
            x = self.clean_prompt(x)
            if x == False:
                return "Not printable"
            x = list(x)
            node_text = ""
            for i in range(6):
                for j in range(6):
                    if x[i * 6 + j] != '0':
                        node_text += x[i * 6 + j]
                    else:
                        node_text += '.'
                node_text += '\n'
            return node_text + f"   [{36 - node_text.count('.')}]   "
        except Exception as e:
            return "Not printable"
        
    def print_node_sudoku_4(self, x):
        try:
            x = self.clean_prompt(x)
            if x == False:
                return "Not printable"
            x = list(x)
            node_text = ""
            for i in range(4):
                for j in range(4):
                    if x[i * 4 + j] != '0':
                        node_text += x[i * 4 + j]
                    else:
                        node_text += '.'
                node_text += '\n'
            return node_text + f"   [{16 - node_text.count('.')}]   "
        except Exception as e:
            return "Not printable"
        
    def get_solutions_g24(self, solutions, root, step):
        if step == 2:
            results = []

            def dfs(node, path, depth):
                if depth == 3:
                    results.append("\n".join([n.task for n in path[1:]]))
                    return

                for child in node.branches:
                    dfs(child, path + [child], depth + 1)

            for child in root.branches:
                dfs(child, [root, child], 1)

            return results, [], True
        else:
            return [], solutions, False
    
    def get_solutions_sudoku(self, solutions, root, step):
        complete_solutions = []
        incomplete_solutions = []
        for solution in solutions:
            puzzle = self.clean_prompt(solution.task)
            if puzzle.count('0') == 0:
                complete_solutions.append(solution.task)
                continue
            if all(len(solution.domains[key]) == 1 for key in solution.domains):
                complete_solution = ""
                for key in solution.domains:
                    complete_solution += solution.domains[key][0]
                complete_solutions.append(self.make_grid(complete_solution, int(m.sqrt(len(complete_solution)))))
                continue
            else:
                incomplete_solutions.append(solution)
        return complete_solutions, incomplete_solutions, True if incomplete_solutions == [] else False
    
    def validate_sudoku_9(self, response, initial_puzzle):
        puzzle = self.clean_prompt(response)
        initial_puzzle = self.clean_prompt(initial_puzzle)
        if (len(puzzle) != 81) | ('0' in puzzle) | (puzzle == False):
            return False
    
        board = [[int(puzzle[i * 9 + j]) for j in range(9)] for i in range(9)]
        
        def all_unique(nums):
            nums = [num for num in nums if num != 0]
            return len(nums) == len(set(nums))
        
        for row in board:
            if not all_unique(row):
                return False
        
        for col in range(9):
            if not all_unique([board[row][col] for row in range(9)]):
                return False
        
        for box_row in range(3):
            for box_col in range(3):
                box = [board[r][c] for r in range(box_row * 3, (box_row + 1) * 3)
                                    for c in range(box_col * 3, (box_col + 1) * 3)]
                if not all_unique(box):
                    return False
        for i in range(81):
            if (initial_puzzle[i] != '0') and (initial_puzzle[i] != puzzle[i]):
                return False
        return True
    
    def validate_sudoku_6(self, puzzle, initial_puzzle):
        puzzle = self.clean_prompt(puzzle)
        initial_puzzle = self.clean_prompt(initial_puzzle)
        if len(puzzle) != 36 or '0' in puzzle:
            return False

        board = [[int(puzzle[i * 6 + j]) for j in range(6)] for i in range(6)]

        def all_unique(nums):
            nums = [num for num in nums if num != 0]
            return len(nums) == len(set(nums))

        for row in board:
            if not all_unique(row):
                return False

        for col in range(6):
            if not all_unique([board[row][col] for row in range(6)]):
                return False

        for box_row in range(3):
            for box_col in range(2):
                box = [board[r][c] for r in range(box_row * 2, (box_row + 1) * 2)
                                    for c in range(box_col * 3, (box_col + 1) * 3)]
                print(box)
                print()
                if not all_unique(box):
                    return False

        for i in range(36):
            if initial_puzzle[i] != '0' and initial_puzzle[i] != puzzle[i]:
                return False

        return True
    
    def validate_sudoku_4(self, puzzle, initial_puzzle):
        puzzle = self.clean_prompt(puzzle)
        initial_puzzle = self.clean_prompt(initial_puzzle)
        if len(puzzle) != 16 or '0' in puzzle:
            return False

        board = [[int(puzzle[i * 4 + j]) for j in range(4)] for i in range(4)]

        def all_unique(nums):
            nums = [num for num in nums if num != 0]
            return len(nums) == len(set(nums))

        for row in board:
            if not all_unique(row):
                return False

        for col in range(4):
            if not all_unique([board[row][col] for row in range(4)]):
                return False

        for box_row in range(2):
            for box_col in range(2):
                box = [board[r][c] for r in range(box_row * 2, (box_row + 1) * 2)
                                    for c in range(box_col * 2, (box_col + 1) * 2)]
                if not all_unique(box):
                    return False

        for i in range(16):
            if initial_puzzle[i] != '0' and initial_puzzle[i] != puzzle[i]:
                return False

        return True

    def validate_g24_ENUM(self, response, initial_task):
        response = response.split('=')[0].strip()
        try:
            if eval(response) != 24:
                return False
        except Exception as e:
            return False
        initial_task = initial_task.split(' ')
        for i in range(len(initial_task)):
            if initial_task[i] not in response:
                return False
            else:
                response.replace(initial_task[i], '')
                print(response)
        return True


    def set_domain_specific_code(self, scd, task_input, branching_strategy):
        if scd["id"] == "g24_scd":
            self.args['peers'] = scd['peers']
            self.args['variables'] = scd['variables']
            self.args['queue'] = self.queue_init(scd['peers'])
            initial_domains = self.set_initial_domains_and_args_g24(task_input)
            self.extract_solutions = self.extract_solutions_g24
            self.set_args = self.set_args_g24
            printer = self.print_node_g24
            if branching_strategy == "BFS_AC3":
                validator = self.validate_g24_BFS_AC3
            else:
                validator = self.validate_g24_ENUM
            get_solutions = self.get_solutions_g24
            return prunner(self.set_domains_g24, self.check_constraints_g24), generator(self.format_prompt_g24), initial_domains, aggregator(printer), validator, get_solutions
        
        if scd["id"]  == "sudoku_9_scd":
            self.args['peers'] = scd['peers']
            self.args['variables'] = scd['variables']
            self.args['domains'] = scd['domains']
            self.args['queue'] = self.queue_init(scd['peers'])
            self.args["new_values"] = {}
            p = prunner(self.set_domains_sudoku_9, self.check_constraints_sudoku)
            initial_domains = self.set_initial_domains_and_args_sudoku_9(task_input, p)
            self.extract_solutions = self.extract_solutions_sudoku
            self.set_args = self.set_args_sudoku_9
            printer = self.print_node_sudoku_9
            validator = self.validate_sudoku_9
            get_solutions = self.get_solutions_sudoku
            return p, generator(self.format_prompt_sudoku_9), initial_domains, aggregator(printer), validator, get_solutions

        if scd["id"] == "sudoku_6_scd":
            self.args['peers'] = scd['peers']
            self.args['variables'] = scd['variables']
            self.args['domains'] = scd['domains']
            self.args['queue'] = self.queue_init(scd['peers'])
            self.args["new_values"] = {}
            p = prunner(self.set_domains_sudoku_6, self.check_constraints_sudoku)
            initial_domains = self.set_initial_domains_and_args_sudoku_6(task_input, p)
            self.extract_solutions = self.extract_solutions_sudoku
            self.set_args = self.set_args_sudoku_6
            printer = self.print_node_sudoku_6
            validator = self.validate_sudoku_6
            get_solutions = self.get_solutions_sudoku
            return p, generator(self.format_prompt_sudoku_6), initial_domains, aggregator(printer), validator, get_solutions
        
        if scd["id"] == "sudoku_4_scd":
            self.args['peers'] = scd['peers']
            self.args['variables'] = scd['variables']
            self.args['domains'] = scd['domains']
            self.args['queue'] = self.queue_init(scd['peers'])
            self.args["new_values"] = {}
            p = prunner(self.set_domains_sudoku_4, self.check_constraints_sudoku)
            initial_domains = self.set_initial_domains_and_args_sudoku_4(task_input, p)
            self.extract_solutions = self.extract_solutions_sudoku
            self.set_args = self.set_args_sudoku_4
            printer = self.print_node_sudoku_4
            validator = self.validate_sudoku_4
            get_solutions = self.get_solutions_sudoku
            return p, generator(self.format_prompt_sudoku_4), initial_domains, aggregator(printer), validator, get_solutions

        else:
            return True, True
