# Python Automation Project 1 - MultiClipboard

import sys
import argparse
import clipboard
import json

"""This Python script implements a MultiClipboard tool that allows 
users to save and retrieve multiple items from their clipboard. 
It provides a command-line interface with four commands: 
save, load, list and delete.

The 'save' command prompts the user to enter a key and saves the 
current clipboard content with that key.
The 'load' command prompts the user to enter a key and retrieves the
corresponding value from the clipboard data, copying it to the clipboard.
The 'list' command displays the entire clipboard data.
The clipboard data is stored in a JSON file for persistence. 
The 'delete' command displays the entire clipboard data.
The script utilizes the argparse library for command-line argument 
parsing and the clipboard library to interact with the clipboard. 
The code includes error handling, input validation
and proper file handling for data storage."""

#####################
# Instructions to use
#####################
# To save type the following in the command line: Python main.py save
# To load type the following in the command line: Python main.py load
# To list type the following in the command line: Python main.py list
# To delete type the following in the command line: Python main.py delete

SAVED_DATA = "clipboard.json"


def save_data(filepath, data):
    """
    Saves the clipboard data to a file in JSON format.

    Args:
        filepath (str): The path to the file.
        data (dict): The data to be saved.

    """
    with open(filepath, "w") as f:
        json.dump(data, f)


def load_data(filepath):
    """
    Loads the clipboard data from a JSON file.

    Args:
        filepath (str): The path to the file.

    Returns:
        dict: The loaded clipboard data.

    """
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid data format in the file.")
        return {}

def process_list_command(data):
    """
    Processes the 'list' command.

    Prints the keys and their corresponding values from the clipboard data.

    Args:
        data (dict): The clipboard data.

    """
    for key, value in data.items():
        print(f"Key: {key}\tValue: {value}")

def process_save_command(data):
    """
    Processes the 'save' command.

    Prompts the user to enter a key and saves the current clipboard content
    with that key in the clipboard data.

    Args:
        data (dict): The clipboard data.

    """
    key = input("Enter a key: ")
    if not key:
        print("Error: Key cannot be empty.")
        return

    if key in data:
        overwrite = input(f"A key with name '{key}' already exists. Do you want to overwrite? (y/n): ")
        if overwrite.lower() != "y":
            print("Save operation canceled.")
            return

    data[key] = clipboard.paste()
    save_data(SAVED_DATA, data)
    print("Data saved successfully.")


def process_load_command(data):
    """
    Processes the 'load' command.

    Prompts the user to enter a key and copies the corresponding value from the
    clipboard data to the clipboard.

    Args:
        data (dict): The clipboard data.

    """
    key = input("Enter a key: ")
    if not key:
        print("Error: Key cannot be empty.")
        return

    if key in data:
        clipboard.copy(data[key])
        print("Data has been copied to clipboard.")
    else:
        print("Key does not exist.")



def process_delete_command(data):
    """
    Processes the 'delete' command.

    Prompts the user to enter a key and deletes the corresponding entry from the clipboard data.

    Args:
        data (dict): The clipboard data.

    """
    key = input("Enter a key: ")
    if not key:
        print("Error: Key cannot be empty.")
        return

    if key in data:
        del data[key]
        save_data(SAVED_DATA, data)
        print("Entry deleted successfully.")
    else:
        print("Key does not exist.")

def main():
    """
    Main function.

    Parses the command-line argument, loads the clipboard data, and processes
    the respective command.

    """
    parser = argparse.ArgumentParser(description="MultiClipboard")
    parser.add_argument("command", choices=["save", "load", "list", "delete"], help="Command to execute")
    args = parser.parse_args()
    command = args.command

    data = load_data(SAVED_DATA)

    if command == "save":
        process_save_command(data)
    elif command == "load":
        process_load_command(data)
    elif command == "list":
        process_list_command(data)
    elif command == "delete":
        process_delete_command(data)

if __name__ == "__main__":
    main()
