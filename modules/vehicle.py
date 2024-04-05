import requests
import json
import random
from modules.vehicleday import Trip, TotalTrip, Parking
from datetime import datetime, timedelta
from dotenv import load_dotenv
from os import getenv
from streamlit import secrets

load_dotenv()
LIQUID_API_KEY = getenv("LIQUID_API_KEY")  # for local
# LIQUID_API_KEY = secrets["LIQUID_API_KEY"]  # both local and cloud deployment


class Vehicle:
    def __init__(self, api_data):
        self.registration_number = api_data.get("registration_number")
        self.art_end_date = api_data.get("art_end_date")
        self.co2_emissions = api_data.get("co2_emissions")
        self.capacity = api_data.get("capacity")
        self.euro_status = api_data.get("euro_status")
        self.marked_for_export = api_data.get("marked_for_export")
        self.fuel_type = api_data.get("fuel_type")
        self.mot_status = api_data.get("mot_status")
        self.revenue_weight = api_data.get("revenue_weight")
        self.colour = api_data.get("colour")
        self.make = api_data.get("make")
        self.type_approval = api_data.get("type_approval")
        self.year_of_manufacture = api_data.get("year_of_manufacture")
        self.tax_due_date = api_data.get("tax_due_date")
        self.tax_status = api_data.get("tax_status")
        self.date_of_last_v5c_issued = api_data.get("date_of_last_v5c_issued")
        self.wheelplan = api_data.get("wheelplan")
        self.month_of_first_dvla_registration = api_data.get(
            "month_of_first_dvla_registration"
        )
        self.month_of_first_registration = api_data.get("month_of_first_registration")
        self.real_driving_emissions = api_data.get("real_driving_emissions")
        self.trips = []
        self.total_trip = []
        self.parking_data = []

    def get_info(self, registration_number):
        url = "http://vesapi.liquid.tech:8010/vehicle-enquiry/v1/vehicles"
        headers = {"x-api-key": LIQUID_API_KEY, "Content-Type": "application/json"}
        payload = json.dumps({"registrationNumber": registration_number})

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            api_data = json.loads(response.text)
            self.__init__(api_data)  # Update the Vehicle object with the new data
            return self
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None

    # def get_info(self, registration_number):
    #     with open("vehicle_database.json", "r") as file:
    #         database = json.load(file)

    #     vehicle_data = database.get(registration_number)
    #     if vehicle_data:
    #         self.__init__(vehicle_data)  # Update the Vehicle object with the new data
    #         return self
    #     else:
    #         print(
    #             f"Error: Vehicle with registration number {registration_number} not found in the database."
    #         )
    #         return None

    def generate_random_trip_data(self):
        # Generate random trip data for the vehicle
        # Replace these values with actual data or more complex logic
        roads = ["Road A", "Road B", "Road C"]
        locations = ["Location X", "Location Y", "Location Z"]
        stops = [2, 3, 1]
        capacity = int(random.uniform(10, 100))
        trip_times = []
        mileage = int(random.uniform(50, 100))
        for _ in range(3):
            start_time = datetime(2024, 4, 4, 8, 0)  # Assuming trip starts at 8:00 AM
            trip_duration = int(random.uniform(30, 120))  # in minutes
            trip_end_time = start_time + timedelta(minutes=trip_duration)
            trip_times.append((start_time, trip_end_time))
        time_in_traffic_jam = int(random.uniform(0, 30))  # in minutes
        time_on_freeway = int(random.uniform(0, 60))  # in minutes

        trip = Trip(
            roads,
            locations,
            stops,
            mileage,
            capacity,
            trip_times,
            time_in_traffic_jam,
            time_on_freeway,
        )
        self.trips.append(trip)
        self.total_trip.add_trip(trip)

    def generate_random_parking_data(self):
        # Generate random parking data for the vehicle
        # Replace these values with actual data or more complex logic
        location = "Parking Location L"
        parking_type = random.choice(["on_street", "underground", "in_silo"])
        time_spent = random.uniform(30, 480)  # in minutes

        # Generate random entry and exit times within the duration of parking
        entry_time = datetime(2024, 4, 4, 8, 0)  # Assuming parking starts at 8:00 AM
        exit_time = entry_time + timedelta(minutes=time_spent)

        parking_data = {
            "location": location,
            "parking_type": parking_type,
            "entry_time": entry_time,
            "exit_time": exit_time,
        }

        self.parking_data.append(parking_data)

    def to_dict(self):
        trips_data = []
        for trip in self.trips:
            trip_dict = {
                "mileage": trip.mileage,
                "roads": trip.roads,
                "locations": trip.locations,
                "stops": trip.stops,
                "capacity": trip.capacity,
                "trip_times": trip.trip_times,
                "time_in_traffic_jam": trip.time_in_traffic_jam,
                "time_on_freeway": trip.time_on_freeway,
            }
            trips_data.append(trip_dict)

        parking_data = []
        for parking in self.parking_data:
            parking_dict = {
                "location": parking["location"],
                "parking_type": parking["parking_type"],
                "entry_time": parking["entry_time"].isoformat(),
                "exit_time": parking["exit_time"].isoformat(),
            }
            parking_data.append(parking_dict)

        return {
            "registration_number": self.registration_number,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "colour": self.colour,
            "trips": trips_data,
            "parking_data": parking_data,
            "total_trip": {
                "total_capacity": self.total_trip.get_total_capacity(),
                "total_trip_time": self.total_trip.get_total_trip_time(),
                "total_time_in_traffic_jam": self.total_trip.get_total_time_in_traffic_jam(),
                "total_time_on_freeway": self.total_trip.get_total_time_on_freeway(),
            },
        }


# if __name__ == "__main__":
#     registration_number = "KCG900V"
#     # Example usage
#     vehicle = Vehicle({})  # Create an empty Vehicle object
#     vehicle_info = vehicle.get_info(registration_number)
#     #
#     if vehicle_info:
#         print(vehicle_info.registration_number)
#         print(vehicle_info.make)
#         print(vehicle_info.tax_status)
#         print(vehicle_info.mot_status)
#         print(vehicle_info.colour)
#         print(vehicle_info.year_of_manufacture)
#         print(vehicle_info.capacity)
#         print(vehicle_info.co2_emissions)
# #
