import json
import os

class SnackEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Snack):
            return {
                'snack_id': obj.snack_id,
                'name': obj.name,
                'price': obj.price,
                'availability': obj.availability
            }
        return super().default(obj)


class Snack:
    def __init__(self, snack_id, name, price, availability):
        self.snack_id = snack_id
        self.name = name
        self.price = price
        self.availability = availability

    def __str__(self):
        return f"{self.name} (ID: {self.snack_id}) - Price: {self.price} - Availability: {'Yes' if self.availability else 'No'}"

def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass  # Ignore decode errors and return an empty dictionary
    return {}


# def save_data(data, file_name):
#     with open(file_name, 'w') as file:
#         json.dump(data, file, indent=4)
def save_data(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4, cls=SnackEncoder)


def add_snack(inventory, snack_id, name, price):
    availability = True
    snack = Snack(snack_id, name, price, availability)
    inventory[snack_id] = snack

def remove_snack(inventory, snack_id):
    if snack_id in inventory:
        del inventory[snack_id]
        print(f"Snack with ID {snack_id} removed from inventory.")
    else:
        print(f"Snack with ID {snack_id} not found in inventory.")

def update_availability(inventory, snack_id, availability):
    if snack_id in inventory:
        inventory[snack_id].availability = availability
        print(f"Availability of snack with ID {snack_id} updated.")
    else:
        print(f"Snack with ID {snack_id} not found in inventory.")

def make_sale(inventory, sales_record, snack_id):
    if snack_id in inventory:
        snack = inventory[snack_id]
        if snack.availability:
            snack.availability = False
            sales_record.append(snack)
            print(f"Sale recorded: {snack}")
        else:
            print("Sorry, this snack is not available.")
    else:
        print(f"Snack with ID {snack_id} not found in inventory.")

def get_int_input(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return get_int_input(prompt)

def main():
    inventory = load_data('db.json')
    sales_record = []

    while True:
        print("\nCanteen Management System")
        print("1. Add Snack")
        print("2. Remove Snack")
        print("3. Update Availability")
        print("4. Make Sale")
        print("5. Exit")

        choice = get_int_input("Enter your choice: ")

        if choice == 1:
            snack_id = get_int_input("Enter Snack ID: ")
            name = input("Enter Snack Name: ")
            price = float(input("Enter Snack Price: "))
            add_snack(inventory, snack_id, name, price)
            save_data(inventory, 'db.json')
        elif choice == 2:
            snack_id = get_int_input("Enter Snack ID to remove: ")
            remove_snack(inventory, snack_id)
            save_data(inventory, 'db.json')
        elif choice == 3:
            snack_id = get_int_input("Enter Snack ID to update availability: ")
            availability = input("Is the snack available? (yes/no): ").lower() == 'yes'
            update_availability(inventory, snack_id, availability)
            save_data(inventory, 'db.json')
        elif choice == 4:

            snack_id = get_int_input("Enter Snack ID sold: ")
            make_sale(inventory, sales_record, snack_id)
            save_data(inventory, 'db.json')
        elif choice == 5:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
