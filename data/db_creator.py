import json
import os


def create_json_db(input_path, output_path):
    """Create a JSON database of registration no.s as objects from a text file with reg no.s list."""
    # TODO: tryuse curl to get list
    with open(input_path, "r") as file:
        lines = file.readlines()
    reg_nos = {}  # initialise empty dict.
    for line in lines:
        key = line.strip()  # Remove trailing newline characters
        reg_nos[key] = {}  # Add key to dict.
    with open(output_path, "w") as outfile:
        json.dump(reg_nos, outfile, indent=2)


if __name__ == "__main__":
    print(f"Current working dir: {os.getcwd()}")
    input_file_path = os.path.join(
        os.getcwd(), "./data/reg_no_list.txt"
    )  # ? use FileBuffer??
    output_file_path = os.path.join(os.getcwd(), "./data/reg_nos.json")
    create_json_db(input_file_path, output_file_path)
