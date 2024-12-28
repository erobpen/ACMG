

class prunner:
    def __init__(self, set_domains, check_constraints):
        self.set_domains = set_domains
        self.check_constraints = check_constraints
        pass

    def revise(self, first_node, second_node, values, args):

        removed_some = False
        removed = []
        for v in values[first_node]:
            satisfies_with_some = False
            for w in values[second_node]:
                satisfies_with_some = self.check_constraints(args, first_node, second_node, v, w)

                if satisfies_with_some:
                    break
            if not satisfies_with_some:
                removed_some = True
                removed.append(v)
                if len(removed) == len(values[first_node]):
                    return False, False
        for v in removed:
            values[first_node].remove(v)

        return values, removed_some
    

    def assign(self, values, args):
        
        # print("values going in the prunner: ")
        # self.print_values_prunner(values)
        queue = args['queue']
        peers = args['peers']
        flag, values = self.set_domains(values)
        if not flag:
            return False
    
        while queue != []:
            tmp_queue = queue.copy()
            tmp_queue.remove(queue[0])
            arc = queue[0]
            arc = list(arc)
            first_node = arc[0] + arc[1]
            second_node = arc[2] + arc[3]
                    
            revision, removed_some = self.revise(first_node, second_node, values, args)
            if revision == False:
                return False
            values = revision

            if removed_some:
                for v in peers[first_node]:
                    arc_to_add = v + first_node
                    if arc_to_add not in queue:
                        tmp_queue.append(arc_to_add)
            queue = tmp_queue

        # print("Satisfies +1")
        # self.print_values_prunner(values)
        return values
    

    def print_values_prunner(self, values):
            string = ""
            counter = 0
            for key in values:
                string += ''.join([str(x) for x in values[key]]) + " "
                counter += 1
                if counter == 9:
                    counter = 0
                    string += '\n'
            print(string)
            return string
    



