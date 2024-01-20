# family_tree.py
"""
Family Tree Implementation in Python

This script defines a simple Tree data structure to represent family relationships.
The Tree class has methods to add nodes, traverse the tree, and retrieve family information.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
import json
import csv

class Person:
    def __init__(self, id, data = None):
        if data == None:
            data = {"name":None, "age":None, "parents_IDs": [], "children_IDs" : []}
        self.id = id
        self.data = data
        self.parents = []
        self.children = []

    def __str__(self):
        return f"{self.id}, {self.data}"

class Family:
    def __init__(self):
        self.root = None
        self.persons_IDs = {}

    def add_person(self, id, child_id = None, data = None):
        if id in self.persons_IDs:
            raise ValueError(f"A person with ID {id} already exists")
        
        new_person = Person(id, data)
        if not self.root:
            self.root = new_person
            self.root.children = None
            return

        child = self.find_person(child_id)
        if not child:
            raise ValueError("The provided child id does not exist")
        elif len(child.parents) >= 2:
            raise ValueError("A person can have at most two parents")
        else:
            new_person.children.append(child)
            child.parents.append(new_person)
            new_person.data["children_IDs"] = [child.id]
            if len(child.data["parents_IDs"]) < 2:
                child.data["parents_IDs"].append(new_person.id)

    def find_person(self, id, node=None):
        if node == None:
            node = self.root

        if node.id == id:
            return node

        for parent in getattr(node, "parents", []):
            result = self.find_person(id, parent)
            if result:
                return result

        return None

    def save_family(self, filename):
        match filename[-1]:
            case "v":
                self.save_to_csv(filename)
            case "n":
                self.save_to_json(filename)

    def save_to_csv(self, filename):
        if not self.root:
            return

        generations = {}
        self._generation_recursion(self.root, 0, generations, usage="s")
        generations = dict(sorted(generations.items(), key=lambda x: int(x[0])))

        with open(filename, "w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['ID', 'name', 'age', 'parents_IDs', 'children_IDs'])
            for id, data in generations.items():
                csv_writer.writerow([id, data['name'], data['age'], data['parents_IDs'], data['children_IDs']])

    def save_to_json(self, filename):
        if not self.root:
            return

        generations = {}
        self._generation_recursion(self.root, 0, generations, usage = "s")
        generations = dict(sorted(generations.items(), key=lambda x: int(x[0])))
        with open(filename, "w") as file:
            json.dump(generations, file, indent=2)

    def load_family(self, filename):
        match filename[-1]:
            case "v":
                self.load_from_csv(filename)
            case "n":
                self.load_from_json(filename)

    def load_from_csv(self, filename):
        with open(filename, "r", newline='') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                id = row.pop("ID")
                converted_row = {key: self.csv_convert(value) for key, value in row.items()}

                if converted_row["children_IDs"] == "None":
                    self.add_person(id, data=converted_row)
                    continue
                self.add_person(id, converted_row["children_IDs"][0], converted_row)

    def load_from_json(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for id, person_data in data.items():
                child_id = person_data["children_IDs"]
                if child_id == None:
                    self.add_person(id, data = person_data)
                    continue
                for child in child_id:
                    self.add_person(id, str(child), person_data)

    def csv_convert(self, value):
        if value == '[None]':
            return [None]
        if len(value) >= 2 and value[0] == "[" and value[-1] == "]":
            value = value[2:-2]
            elements = [item.strip() for item in value.split("', '")]
            return elements
        return value

    def print_person(self, id):
        person = self.find_person(id)
        print(person)

    def print_related(self, node = None, limit = 2 ):
        if not node:
            node = self.root
        else:
            node = self.find_person(node)
        
        for up_down in (True, False):
            ancestors = {}
            self._generation_recursion(node, 0, ancestors, limit = limit, up_down = up_down)

            ancestors = dict(sorted(ancestors.items(), key=lambda x: int(x[0]), reverse=up_down))
            
            for generation, nodes in ancestors.items():
                nodes = dict(sorted(nodes.items(), key=lambda x: int(x[0])))
                match generation:
                    case 0:
                        if up_down:
                            continue
                        print(f"Person:", end=" ")
                    case 1:
                        print(f"{("Parents" if up_down else "Children")}:", end=" ")
                    case 2:
                        print(f"{("Grandparents" if up_down else "Grandhildren")}:", end=" ")
                    case _:
                        print((int(generation)-2)*"Great-",f"{("grandparents" if up_down else "children")}: ", sep="" ,end=" ")
                
                print(*[f"{node["name"]} |" for _, node in nodes.items()])
                print("    |")


    def _generation_recursion(self, node, generation, generations, limit = None, usage = "p", up_down = None):
        if usage == "p" and generation not in generations:
            generations[generation] = {}

        match usage:
            case "s":
                generations.update({node.id:node.data})
                for parent in sorted(getattr(node, "parents", []), key=lambda x: x.id):
                    self._generation_recursion(parent, generation + 1, generations, limit=(limit - 1 if limit else None), usage=usage , up_down=up_down)
            case "p":
                generations[generation].update({node.id: node.data})
                if limit == 0:
                    return
                for parent in sorted(getattr(node, "parents" if up_down else "children", []), key=lambda x: x.id):
                    self._generation_recursion(parent, generation + 1, generations, limit=(limit - 1 if limit else None), usage=usage , up_down=up_down)

    def add_n_persons(self, n, count, count_gen):
        if n == 0:
            return count
        if count != 0: 
            self.add_person(count, count_gen)
            self.add_person(count + 1, count_gen)
            count = self.add_n_persons(n-1, count + 2, count_gen + 1)
        else:
            self.add_person(count)
            count_gen -= 1
            count = self.add_n_persons(n-1, count + 1, count_gen + 1)
        return count

    def add_n_gen(self,n):
        self.add_n_persons(2**n, 0, 0)
