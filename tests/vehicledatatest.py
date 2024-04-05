import requests
import json


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

    def get_info(self, registration_number):
        url = "http://vesapi.liquid.tech:8010/vehicle-enquiry/v1/vehicles"
        headers = {"x-api-key": "Hr*ugf(N*&YH", "Content-Type": "application/json"}
        payload = json.dumps({"registrationNumber": registration_number})

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            api_data = json.loads(response.text)
            self.__init__(api_data)  # Update the Vehicle object with the new data
            return self
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None


# Example usage
registration_number = "KCG900V"
vehicle = Vehicle({})  # Create an empty Vehicle object
vehicle_info = vehicle.get_info(registration_number)

if vehicle_info:
    print(vehicle_info.registration_number)
    print(vehicle_info.make)
    print(vehicle_info.tax_status)
    print(vehicle_info.mot_status)
    print(vehicle_info.colour)
    print(vehicle_info.year_of_manufacture)
    print(vehicle_info.engine_capacity)
    print(vehicle_info.co2_emissions)
