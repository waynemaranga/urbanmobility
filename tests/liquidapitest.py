import requests
import json
from dotenv import load_dotenv
from os import getenv
from streamlit import secrets

load_dotenv()
# LIQUID_API_KEY = getenv("LIQUID_API_KEY")  # for local
LIQUID_API_KEY = secrets["LIQUID_API_KEY"]  # both local and cloud deployment


class Vehicle:
    def __init__(self, api_data):
        self.registration_number = api_data.get("registrationNumber")
        self.art_end_date = api_data.get("artEndDate")
        self.co2_emissions = api_data.get("co2Emissions")
        self.engine_capacity = api_data.get("engineCapacity")
        self.euro_status = api_data.get("euroStatus")
        self.marked_for_export = api_data.get("markedForExport")
        self.fuel_type = api_data.get("fuelType")
        self.mot_status = api_data.get("motStatus")
        self.revenue_weight = api_data.get("revenueWeight")
        self.colour = api_data.get("colour")
        self.make = api_data.get("make")
        self.type_approval = api_data.get("typeApproval")
        self.year_of_manufacture = api_data.get("yearOfManufacture")
        self.tax_due_date = api_data.get("taxDueDate")
        self.tax_status = api_data.get("taxStatus")
        self.date_of_last_v5c_issued = api_data.get("dateOfLastV5CIssued")
        self.wheelplan = api_data.get("wheelplan")
        self.month_of_first_dvla_registration = api_data.get(
            "monthOfFirstDvlaRegistration"
        )
        self.month_of_first_registration = api_data.get("monthOfFirstRegistration")
        self.real_driving_emissions = api_data.get("realDrivingEmissions")


def get_vehicle_info(registration_number):
    url = "http://vesapi.liquid.tech:8010/vehicle-enquiry/v1/vehicles"
    headers = {"x-api-key": LIQUID_API_KEY, "Content-Type": "application/json"}
    payload = json.dumps({"registrationNumber": registration_number})

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        api_data = json.loads(response.text)
        return Vehicle(api_data)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# Example usage
registration_number = "KDL194E"
vehicle = get_vehicle_info(registration_number)


def print_vehicle_data(vehicle_data):
    for reg_num, data in vehicle_data.items():
        print(f"Registration Number: {reg_num}")
        for attr, value in data.items():
            if (
                attr != "registration_number"
            ):  # Skip registration_number, as it's already printed
                print(f"{attr.replace('_', ' ').capitalize()}: {value}")
        print()  # Print an empty line to separate vehicles


# Example usage
vehicle_data = {
    "KAA051O": {
        "registration_number": "KAA051O",
        "make": "Ford",
        "tax_status": "Taxed",
    },
    "KAA379O": {
        "registration_number": "KAA379O",
        "make": "Audi",
        "tax_status": "Untaxed",
    },
    # ... (other vehicles)
}

print_vehicle_data(vehicle_data)


# if vehicle:
#     print(vehicle.registration_number)
#     print(vehicle.make)
#     print(vehicle.tax_status)
# else:
#     print("Failed to retrieve vehicle information.")
