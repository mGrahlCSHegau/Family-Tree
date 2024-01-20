# example_script.py
"""
Family Tree Implementation in Python

This script showcases the usage of the Tree data structure from family_tree.py.

Author: Merlin Grahl
Date: 15/Jan/2024 | 16:00(MEZ)
"""
from family_tree import Family
family = Family()

#this checks the if a tree alredy exists
if "/workspaces/Family-Tree/family_tree/family_info.csv":
    family.load_family("/workspaces/Family-Tree/family_tree/family_info.csv")
else:
    family.add_n_gen(8)         #this funktion adds n generations from the root to 8 previus generations. (only IDs no other data()

family.print_person("4")        #this funktion prints id and data of a given person.

family.print_related("20",3)    #this funktion prints the ancestors and descendants of a given persons id to a given level.

family.save_family("/workspaces/Family-Tree/family_tree/family_info.csv")