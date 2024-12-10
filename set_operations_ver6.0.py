import tkinter as tk
from tkinter import font as tkFont
from tkinter import messagebox

class SetOperationsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Set Operations")

        # Define Font Classes
        self.large_font = tkFont.Font(family="Arial", size=16, weight="normal")
        self.subtext_font = tkFont.Font(family="Arial", size=12, weight="normal")

        # Initialize variables
        self.universal_set = tk.StringVar()
        self.set_a = tk.StringVar()
        self.set_b = tk.StringVar()
        self.result = tk.StringVar()

        # Header
        tk.Label(root, text="Enter the sets. \nElements should be separated by comma.", font=self.subtext_font).grid(row=0, column=0, columnspan=2)

        # Universal Set
        tk.Label(root, text="Universal Set:", font=self.large_font).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.universal_entry = tk.Entry(root, textvariable=self.universal_set, font=self.large_font)
        self.universal_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        # Set A
        tk.Label(root, text="Set A:", font=self.large_font).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.set_a_entry = tk.Entry(root, textvariable=self.set_a, font=self.large_font)
        self.set_a_entry.grid(row=2, column=1, sticky="w",padx=5, pady=5)
        
        # Set B
        tk.Label(root, text="Set B:", font=self.large_font).grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.set_b_entry = tk.Entry(root, textvariable=self.set_b, font=self.large_font)
        self.set_b_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        # Set Operations Dropdown
        tk.Label(root, text="Select Operation:", font=self.large_font).grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.operation_var = tk.StringVar()
        self.operation_var.set("Choose an operation")
        self.operations_menu = tk.OptionMenu(root, self.operation_var, "Complement", "Union", "Intersection",
                                             "Difference", "Symmetric Difference", "Cartesian Product", "Power Set",
                                             command=self.toggle_target_menu)
        self.operations_menu.config(font=self.subtext_font)
        self.operations_menu.grid(row=4, column=1, sticky="e", padx=5, pady=5)
        
        # Target Set Dropdown for Complement/Power Set
        tk.Label(root, text="Select Target Set:", font=self.large_font).grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.target_var = tk.StringVar()
        self.target_var.set("Choose a set")
        self.target_menu = tk.OptionMenu(root, self.target_var, "Set A", "Set B")
        self.target_menu.config(font=self.subtext_font)
        self.target_menu.grid(row=5, column=1, sticky="e", padx=5, pady=5)
        self.target_menu.config(state="disabled")  # Initially disabled

        # Execute Button
        self.execute_button = tk.Button(root, text="Execute Operation", command=self.execute_operation, font=self.large_font)
        self.execute_button.grid(row=6, column=1, pady=10)
        
        # Result
        tk.Label(root, text="Result:", font=self.large_font).grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.result_label = tk.Label(root, textvariable=self.result, wraplength=250, font=self.large_font)
        self.result_label.grid(row=7, column=1, padx=5, pady=5)

        # Retry Button
        self.retry_button = tk.Button(root, text="Retry", command=self.retry, font=self.large_font)
        self.retry_button.grid(row=8, column=1, pady=5)

        # Footer
        tk.Label(root, text="Bagon | Fontanilla | Fernandez | Medalla | Zapico", font=self.subtext_font).grid(row=9, column=0, columnspan=3)

    def toggle_target_menu(self, operation):
        # Enable or disable target set selection based on operation type.
        if operation in ["Complement", "Power Set"]:
            self.target_menu.config(state="normal")  # Enable for Complement and Power Set
        else:
            self.target_menu.config(state="disabled")  # Disable for other operations
            self.target_var.set("Choose a set")  # Reset target selection

    def validate_set_input(self, set_input):
        # Validate individual set input to ensure it is non-empty, unique, and properly formatted.
        set_elements = set_input.replace(" ", "").split(",")
        set_elements = [element for element in set_elements if element]

        if not set_elements:
            return False, "Set cannot be empty."

        if len(set_elements) != len(set(set_elements)):
            return False, "Duplicate elements are not allowed."

        return True, set(set_elements)

    def validate_inputs(self):
        # Validate universal set, set A, and set B. Return appropriate Error Messages
        universal_set_str = self.universal_set.get()
        set_a_str = self.set_a.get()
        set_b_str = self.set_b.get()
        
        valid_universal, universal_data = self.validate_set_input(universal_set_str)
        if not valid_universal:
            messagebox.showerror("Validation Error", "Universal Set is invalid: " + universal_data)
            return False

        valid_set_a, set_a_data = self.validate_set_input(set_a_str)
        if not valid_set_a:
            messagebox.showerror("Validation Error", "Set A is invalid: " + set_a_data)
            return False

        valid_set_b, set_b_data = self.validate_set_input(set_b_str)
        if not valid_set_b:
            messagebox.showerror("Validation Error", "Set B is invalid: " + set_b_data)
            return False

        # Ensure Set A and Set B are subsets of the Universal Set
        if not set_a_data.issubset(universal_data):
            messagebox.showerror("Validation Error", "Set A contains elements not in the Universal Set.")
            return False
        if not set_b_data.issubset(universal_data):
            messagebox.showerror("Validation Error", "Set B contains elements not in the Universal Set.")
            return False

        # Store validated sets for further use
        self.universal_set_data = universal_data
        self.set_a_data = set_a_data
        self.set_b_data = set_b_data
        return True

    def parse_input(self, input):
        parsed_set = set()
        input = input.replace(" ", "").split(",")
        parsed_set = {element for element in input}
        return parsed_set

    def execute_operation(self):
        # Execute selected set operation if inputs are valid.
        if not self.validate_inputs():
            return
        
        universal_set = self.parse_input(self.universal_set.get())
        set_a = self.parse_input(self.set_a.get())
        set_b = self.parse_input(self.set_b.get())

        # Perform selected operation
        operation = self.operation_var.get()
        target = self.target_var.get() if operation in ["Complement", "Power Set"] else None

        if target == "Set A":
            selected_set = set_a
        elif target == "Set B":
            selected_set = set_b
        elif target == "Universal Set":
            selected_set = universal_set
        else:
            selected_set = None

        # Perform the operation and check if result is empty
        if operation == "Complement" and selected_set is not None:
            result_set = self.complement(set_a, set_b, universal_set, target)
        elif operation == "Union":
            result_set = self.union(set_a, set_b)
        elif operation == "Intersection":
            result_set = self.intersection(set_a, set_b)
        elif operation == "Difference":
            result_set = self.difference(set_a, set_b)
        elif operation == "Symmetric Difference":
            result_set = self.symmetric_difference(set_a, set_b)
        elif operation == "Cartesian Product":
            result_set = self.cartesian_product(set_a, set_b)
        elif operation == "Power Set" and selected_set is not None:
            result_set = self.power_set(set_a, set_b, target)
        else:
            messagebox.showwarning("Invalid Selection", "Please select a valid operation and target set if required.")
            return
        # Implement custom text, para di malito user when returning null set
        # Check if the result is an empty set and display custom text if true
        if not result_set:
            self.result.set("The result is an empty set.")
        else:
            # Otherwise, display the result normally
            self.result.set(f"{operation}: {result_set}")
            
    def complement(self, set_a, set_b, universal_set, target):
        if target == "Set A":
            complement_set = self.difference(universal_set, set_a)
        elif target == "Set B":
            complement_set = self.difference(universal_set, set_b)
        return complement_set
            
    def union(self, set_a, set_b):
        result = set()
        for element in set_a:
            result.add(element)
        for element in set_b:
            if element not in result:
                result.add(element)
        return result
    
    def intersection(self, set_a, set_b):
        result = set()
        for element in set_a:
            if element in set_b:
                result.add(element)
        return result
    
    def difference(self, set_a, set_b):
        result = set()
        for element in set_a:
            if element not in set_b:
                result.add(element)
        return result

    def symmetric_difference(self, set_a, set_b):
        result = set()
        for element in set_a:
            if element not in set_b:
                result.add(element)
        for element in set_b:
            if element not in set_a:
                result.add(element)
        return result
    
    def cartesian_product(self, set_a, set_b):
        result = set()
        for elementA in set_a:
            for elementB in set_b:
                result.add((elementA, elementB))
        return result
    
    def power_set(self, set_a, set_b, target):
        
        def powerpower(input_set):
            if len(input_set) == 0:   # Base case: the power set of an empty set is a set containing the empty set
                return [set()]
            first_elem = input_set[0]  # Get the first element and the rest of the set
            rest = input_set[1:]
            
            rest_powerset = powerpower(rest)  # Recursively compute the power set of the rest of the set
            
            # Combine the subsets: add the first element to each subset 
            # in the power set of the rest of the set
            with_first_elem = [subset | {first_elem} for subset in rest_powerset]  

            # Return the combination of both sets (with and without the first element)
            return rest_powerset + with_first_elem

        if target == 'Set A':
            input_set = [element for element in set_a]
            return powerpower(input_set)
        elif target == 'Set B':
            input_set = [element for element in set_b]
            return powerpower(input_set)

    def retry(self):
        # Clear input fields and reset variables.
        self.universal_set.set("")
        self.set_a.set("")
        self.set_b.set("")
        self.result.set("")
        self.operation_var.set("Choose an operation")
        self.target_var.set("Choose a set")
        self.target_menu.config(state="disabled")  # Reset target menu state

if __name__ == "__main__":
    root = tk.Tk()
    app = SetOperationsApp(root)
    root.mainloop()
