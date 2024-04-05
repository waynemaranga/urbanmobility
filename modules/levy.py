from modules.vehicle import Vehicle
from modules.vehicleday import Trip
from datetime import datetime, timedelta

# Define rates for driver's levy features
FEATURE_RATES = {
    "capacity": 0.05,  # Rate per cc
    "fuel_type": {"petrol": 0.1, "diesel": 0.15},  # Rate per liter
    "tax_status": {"Taxed": 0.2, "Unpaid": 0.3},  # Rate based on tax status
    "wheelplan": {
        "2 AXLE RIGID BODY": 0.2,
        "4 AXLE RIGID BODY": 0.3,
    },  # Rate based on wheel plan
}

# Define rates for carbon levy features
CARBON_LEVY_RATES = {
    "co2_emissions": 0.01,  # Rate per gram of CO2 emissions
    "real_driving_emissions": 0.02,  # Rate per gram of real driving emissions
}


def calculate_driver_levy(vehicle_info, trip):
    # Calculate driver's levy based on trip data and vehicle information
    driver_levy = 0

    # Engine displacement
    engine_displacement_rate = FEATURE_RATES.get(
        "engine_displacement", 0
    )  # Use 0 as a placeholder
    if engine_displacement_rate is not None:
        driver_levy += engine_displacement_rate * (vehicle_info.capacity or 0)

    # Fuel type
    fuel_type_rate = FEATURE_RATES.get("fuel_type", {}).get(
        vehicle_info.fuel_type, 0
    )  # Use 0 as a placeholder
    if fuel_type_rate is not None:
        driver_levy += fuel_type_rate * trip.capacity

    # Tax status
    tax_status_rate = FEATURE_RATES.get("tax_status", {}).get(
        vehicle_info.tax_status, 0
    )  # Use 0 as a placeholder
    if tax_status_rate is not None:
        driver_levy += tax_status_rate

    # Wheel plan
    wheel_plan_rate = FEATURE_RATES.get("wheel_plan", {}).get(
        vehicle_info.wheelplan, 0
    )  # Use 0 as a placeholder
    if wheel_plan_rate is not None:
        driver_levy += wheel_plan_rate

    return driver_levy


def calculate_carbon_levy(vehicle_info, trip):
    # Calculate carbon levy based on trip data, vehicle information, and carbon-related factors
    carbon_levy = calculate_driver_levy(vehicle_info, trip)

    # CO2 emissions
    co2_emissions_rate = CARBON_LEVY_RATES.get(
        "co2_emissions", 0
    )  # Use 0 as a placeholder
    if co2_emissions_rate is not None:
        carbon_levy += co2_emissions_rate * (vehicle_info.co2_emissions or 0)

    # Real driving emissions (add your calculation logic here)

    return carbon_levy


def generate_driver_levy_info(vehicle_info, trip):
    # Generate driver's levy information
    driver_levy_amount = calculate_driver_levy(vehicle_info, trip)
    driver_levy_info = {
        "registration_number": vehicle_info.registration_number,
        "trip_data": {
            "mileage": trip.capacity,
            "time_in_traffic_jam": trip.time_in_traffic_jam,
            "time_on_freeway": trip.time_on_freeway,
        },
        "driver_levy_amount": driver_levy_amount,
    }
    return driver_levy_info


def generate_carbon_levy_info(vehicle_info, trip):
    # Generate carbon levy information
    carbon_levy_amount = calculate_carbon_levy(vehicle_info, trip)
    carbon_levy_info = {
        "registration_number": vehicle_info.registration_number,
        "trip_data": {
            "mileage": trip.capacity,
            "time_in_traffic_jam": trip.time_in_traffic_jam,
            "time_on_freeway": trip.time_on_freeway,
        },
        "carbon_levy_amount": carbon_levy_amount,
    }
    return carbon_levy_info


# if __name__ == "main":
#   vehicle_info = Vehicle({})  # Replace {} with actual vehicle data
#   trip = Trip([], [], [], 0, [], 0, 0)  # Replace [] and 0s with actual trip data
#   driver_levy_info = generate_driver_levy_info(vehicle_info, trip)
#   carbon_levy_info = generate_carbon_levy_info(vehicle_info, trip)

#   print(driver_levy_info)
#   print(carbon_levy_info)
