class node:
    def __init__(self, id, task, domains, messages):
        self.id = id
        self.task = task
        self.domains = domains
        self.messages = messages
        self.branches = []

    def add_child(self, child_node):
        self.branches.append(child_node)
        return child_node

    def __repr__(self):
        return f"TreeNode(task={self.task})"

    def print_tree(self, level=0):
        indent = " " * (level * 2)
        print(f"{indent}{self.task.strip()}")
        for child in self.branches:
            child.print_tree(level + 1)

    def add_nodes_to_tree(self, root, parent_id, nodes):
        def find_node(node, id):
            if node.id == id:
                return node
            for child in node.branches:
                result = find_node(child, id)
                if result is not None:
                    return result
            return None

        parent_node = find_node(root, parent_id)
        if parent_node is not None:
            for new_node in nodes:
                parent_node.add_child(new_node)
        else:
            print(f"Parent id '{parent_id}' not found in the tree.")


if __name__ == "__main__":

    root = node('root_task', 'root_domain', 'root_message')
    child1 = node('child1_task', 'child1_domain', 'child1_message')
    child2 = node('child2_task', 'child2_domain', 'child2_message')
    root.add_child(child1)
    root.add_child(child2)

    root.add_nodes_to_tree(root, 'child1_task', 'child3_task', 'child3_domain', 'child3_message')
    root.print_tree()
