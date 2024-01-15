# example_script.py
from family_tree import Tree

def main():
    # Create a family tree
    family_tree = Tree()

    # Add nodes to the family tree
    family_tree.add_node(None, "stev")
    family_tree.add_node("Parent", "Child")
    family_tree.add_node("Grandparent", "Aunt")
    family_tree.add_node("Aunt", "Cousin")
    family_tree.add_node("Parent", "Sibling")
    
    # Display family information
    print("Family Information:")
    print(family_tree.get_family_info("Child"))

    # Save the family tree to a file
    family_tree.save_to_file("family_tree.json")
    print("Family tree saved to family_tree.json")

    # Load the family tree from the file
    loaded_tree = Tree()
    loaded_tree.load_from_file("family_tree.json")

    # Display family information after loading from the file
    print("\nFamily Information (After Loading):")
    print(loaded_tree.get_family_info("Child"))

if __name__ == "__main__":
    main()
