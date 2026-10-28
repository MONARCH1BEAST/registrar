"""Lazy menu for all five Advanced Python Programming modules.
Each choice imports only the demo that the student selected.
"""

import importlib

MENU = {
    "1": ("Constructor, destructor, abstract class", "m1_oop.person"),
    "2": ("Class vs instance vars, encapsulation, methods", "m1_oop.student"),
    "3": ("Inheritance types and polymorphism", "m1_oop.special"),
    "4": ("Operator overloading", "m1_oop.operators"),
    "5": ("lambda, map, filter, reduce, recursion", "m2_functional.functional_tools"),
    "6": ("Iterators and generators", "m2_functional.iterators_gens"),
    "7": ("Decorators", "m2_functional.decorators"),
    "8": ("Context manager and metaclass", "m2_functional.context_meta"),
    "9": ("Scope and dynamic typing", "m2_functional.scope_demo"),
    "10": ("Text, CSV, JSON, binary files", "m3_data.files"),
    "11": ("Exceptions and assertions", "m3_data.exceptions"),
    "12": ("SQLite CRUD", "m3_data.database"),
    "13": ("MySQL intro", "m3_data.mysql_demo"),
    "14": ("Threads, lock, process", "m4_network.threads"),
    "15": ("Socket server (blocks, use its own terminal)", "m4_network.server"),
    "16": ("Socket client", "m4_network.client"),
    "17": ("requests, scraping, email", "m4_network.web_tools"),
    "18": ("Tkinter app", "m5_apps.gui"),
    "19": ("Flask app", "m5_apps.web"),
}


def show_menu():
    """Print the available demos without importing their modules."""
    for number, item in MENU.items():
        print(number + ". " + item[0])
    print("0. Exit")


def run_choice(choice):
    """Import one selected module only after the student chooses it."""
    if choice not in MENU:
        print("Choose a number from the list")
        return
    module = importlib.import_module(MENU[choice][1])
    module.demo()


def main():
    """Start logging and keep showing the menu until the user exits."""
    from m3_data.logger import setup_logging
    setup_logging()
    while True:
        show_menu()
        choice = input("Choose a demo: ").strip()
        if choice == "0":
            break
        run_choice(choice)


def demo():
    """Expose the menu as a runnable demonstration."""
    main()


if __name__ == "__main__":
    demo()
