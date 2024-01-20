# example_script.py
"""
Family Tree Implementation in Python

This script showcases the usage of the Tree data structure from family_tree.py.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
from family_tree import Family
family = Family()

if "/workspaces/Family-Tree/family_tree/family_info.csv":
    family.load_family("/workspaces/Family-Tree/family_tree/family_info.csv")
else:
    family.add_n_gen(8)

#family.print_person("4")

family.print_related("4")

family.save_family("/workspaces/Family-Tree/family_tree/family_info.json")