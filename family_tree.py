# family_tree.py
import json

class TreeNode:
    def __init__(self, data, parent=None):
        self.data = data
        self.parent = parent
        self.children = []

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, parent, child_data):
        if not self.root:
            self.root = TreeNode(parent)
        parent_node = self.find_node(self.root, parent)
        if parent_node:
            child_node = TreeNode(child_data, parent=parent_node)
            parent_node.children.append(child_node)
        else:
            raise ValueError(f"Parent {parent} not found in the tree.")

    def find_node(self, node, data):
        if node.data == data:
            return node
        for child in node.children:
            result = self.find_node(child, data)
            if result:
                return result
        return None

    def get_family_info(self, person_data):
        person_node = self.find_node(self.root, person_data)
        if person_node:
            parents = [parent.data for parent in person_node.parent.children] if person_node.parent else None
            grandparents = [grandparent.data for grandparent in self.get_grandparents(person_node)] if person_node.parent else None
            children = [child.data for child in person_node.children] if person_node.children else None
            grandchildren = [grandchild.data for child in person_node.children for grandchild in child.children] if person_node.children else None

            return {
                "Person": person_data,
                "Children": children,
            }
        else:
            return None

    def save_to_file(self, filename="family_tree.json"):
        data_to_save = self._serialize_tree(self.root)
        with open(filename, "w") as file:
            json.dump(data_to_save, file, indent=2)

    def load_from_file(self, filename="family_tree.json"):
        with open(filename, "r") as file:
            data = json.load(file)
        self.root = self._deserialize_tree(data)

    def _serialize_tree(self, node):
        if not node:
            return None

        serialized_node = {"data": node.data}
        if node.children:
            serialized_node["children"] = [self._serialize_tree(child) for child in node.children]

        return serialized_node

    def _deserialize_tree(self, data):
        if not data:
            return None

        node = TreeNode(data["data"])
        if "children" in data:
            node.children = [self._deserialize_tree(child_data) for child_data in data["children"]]

        return node