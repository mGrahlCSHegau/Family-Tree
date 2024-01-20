# example_script.py
"""
Family Tree Implementation in Python

This script showcases the usage of the Tree data structure from family_tree.py.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
from family_tree import Family
family = Family()

if "/workspaces/Family-Tree/family_tree/family_info.json":
    family.load_family("/workspaces/Family-Tree/family_tree/family_info.json")
else:
    family.add_n_gen(8)

family.print_person("5")

family.print_generations()

family.save_family("/workspaces/Family-Tree/family_tree/family_info.json")