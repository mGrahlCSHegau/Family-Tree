# example_script.py
"""
Family Tree Implementation in Python

This script showcases the usage of the Tree data structure from family_tree.py.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
from family_tree import Family
family = Family()

#family.add_n_gen(8)
family.load_family("/workspaces/Family-Tree/family_tree/family_tree.json")
family.print_generations()
family.save_family("/workspaces/Family-Tree/family_tree/family_tree.json")
