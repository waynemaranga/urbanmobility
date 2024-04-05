import json
from modules.vehicle import Vehicle
from tqdm import tqdm
import os
import pandas as pd
from data.db_creator import create_json_db

# from modules.bot import Bot
# from datetime import datetime, timedelta

# Create json database
print(f"Current working dir: {os.getcwd()}")
input_file_path = os.path.join(os.getcwd(), "./data/reg_no_list.txt")  # ? use FileBuffer?? # fmt: skip
output_file_path = os.path.join(os.getcwd(), "./data/reg_nos.json")
create_json_db(input_file_path, output_file_path)

# File paths for database files in the ./data/ directory
input_db = os.path.join("data", "reg_nos.json")
output_db = os.path.join("data", "vehicle_db.json")


def populate_db(input_db, output_db):
    # Load the database from the JSON file
    with open(input_db, "r") as file:
        reg_nos = json.load(file)

    # Iterate through the registration numbers and populate the database
    registration_numbers = list(reg_nos.keys())
    vehicle_database = {}
    for registration_number in tqdm(
        registration_numbers, desc="Populating database..."
    ):
        vehicle = Vehicle({})
        vehicle_info = vehicle.get_info(registration_number)

        if vehicle_info:
            vehicle_database[registration_number] = {
                "registration_number": vehicle_info.registration_number,
                "make": vehicle_info.make,
                "engine_capacity": vehicle_info.capacity,
                "fuel_type": vehicle_info.fuel_type,
                "year_of_manufacture": vehicle_info.year_of_manufacture,
                "wheelplan": vehicle_info.wheelplan,
                "colour": vehicle_info.colour,
                "co2_emissions": vehicle_info.co2_emissions,
                "real_driving_emissions": vehicle_info.real_driving_emissions,
                "revenue_weight": vehicle_info.revenue_weight,
                "type_approval": vehicle_info.type_approval,
                "euro_status": vehicle_info.euro_status,
                "mot_status": vehicle_info.mot_status,
                "tax_status": vehicle_info.tax_status,
                "tax_due_date": vehicle_info.tax_due_date,
                "marked_for_export": vehicle_info.marked_for_export,
                "month_of_first_dvla_registration": vehicle_info.month_of_first_dvla_registration,
                "date_of_last_v5c_issued": vehicle_info.date_of_last_v5c_issued,
                "art_end_date": vehicle_info.art_end_date,
            }
        else:
            print(
                f"Error: Failed to retrieve data for registration number {registration_number}"
            )

    # Save the populated database to the JSON file
    with open(output_db, "w") as file:
        json.dump(vehicle_database, file, indent=2)


def create_dataframe(output_db):
    with open(output_db, "r") as file:
        vehicle_database = json.load(file)

    vehicle_data_list = []
    for vehicle_data in vehicle_database.values():
        vehicle_data_list.append(vehicle_data)

    df = pd.DataFrame(vehicle_data_list)
    return df


# Example usage
if __name__ == "__main__":
    populate_db(input_db, output_db)
    vehicle_df = create_dataframe(output_db)
    print(vehicle_df.head())

    # bot = Bot(
    #     user="What are the most common car types in this database?",
    #     assistant="",
    #     dataframe=vehicle_df,
    # )

    # response = bot.create_completion()
    # print(response)


# TODO:

# - make data categories, like emmission data should be c02 capacity and other info, and tax data should be tax status and tax due date
# - make documenation for the different vehicle data info
