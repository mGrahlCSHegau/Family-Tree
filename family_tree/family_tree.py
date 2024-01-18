# family_tree.py
"""
Family Tree Implementation in Python

This script defines a simple Tree data structure to represent family relationships.
The Tree class has methods to add nodes, traverse the tree, and retrieve family information.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
import json

class Person:
    def __init__(self, id, data = None):
        if not data:
            data = {"name":None, "age":None, "parents_IDs": None, "child_ID" : None}
        self.id = id
        self.data = data
        self.parents = []

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
            return

        child = self.find_person(child_id)
        if not child:
            raise ValueError("The provided child id does not exist")
        elif len(child.parents) >= 2:
            raise ValueError("A person can have at most two parents")
        else:
            child.parents.append(new_person)
            new_person.data["child_ID"] = child.id
            
    
    def find_person(self, id, node=None):
        if not node:
            node = self.root

        if node.id == id:
            return node

        for parent in getattr(node, "parents", []):
            result = self.find_person(id, parent)
            if result:
                return result

        return None

    def save_family(self, filename):
        if not self.root:
            return

        generations = {}
        self._gen_recrusion(self.root, 0, generations, "s")

        with open(filename, "w") as file:
            json.dump(generations, file, indent=2)

    def load_family(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for gen, persons_data in data.items():
                for person_data in persons_data:
                    for person_id in person_data.keys():
                        person_data = person_data[str(person_id)]
                        child_id = person_data["child_ID"]
                        if child_id == None:
                            self.add_person(person_id, data = person_data)
                            continue
                        self.add_person(person_id, str(child_id), person_data)

    def print_generations(self):
        if not self.root:
            return

        generations = {}
        self._gen_recrusion(self.root, 0, generations)
        
        for generation, nodes in generations.items():
            print(f"Generation {generation}:", ', '.join(sorted(str(node) for node in nodes)))

    def _gen_recrusion(self, node, generation, generations, usage = "p"):
        if generation not in generations:
            generations[generation] = []

        match usage:
            case "p":
                generations[generation].append(node.id)
            case "s":
                generations[generation].append({node.id: node.data})

        for parent in sorted(getattr(node, "parents", []), key=lambda x: x.id):
            self._gen_recrusion(parent, generation + 1, generations, usage)
    
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
