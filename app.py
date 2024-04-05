import streamlit as st
from modules.vehicle import Vehicle
from modules.bot import Bot
from st_inputs import reg_no_input
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
from modules.vehicleday import Trip, TotalTrip, Parking
import random
from datetime import datetime, timedelta  # FIXME
from modules.at_sms import SMS
from modules.levy import generate_driver_levy_info, generate_carbon_levy_info
from populate import populate_db, create_dataframe, input_db, output_db

st.set_page_config(page_icon="🚗", page_title="Urban&Mobile", layout="centered")
# -- Populate the database --

populate_db(input_db, output_db)  # FIXME : HOTFIX

# -- Title --
st.title("Urban&Mobile: urbanmobility.streamlit.app")

# -- Section: Vehicle Information --
st.header("🚗 Vehicle Info")
# input should give registration number list as a dropdown
given_reg = reg_no_input("Enter registration number", "vehicle_info")

if given_reg:
    # print(given_reg)
    # st.write(given_reg)
    vehicle = Vehicle({})  # Create an empty Vehicle object
    vehicle_info = vehicle.get_info(given_reg)

    if vehicle_info:

        with st.expander("Vehicle info"):
            st.write(f"Registration Number: {vehicle_info.registration_number}")
            st.write(f"Make: {vehicle_info.make}")
            st.write(f"Tax Status: {vehicle_info.tax_status}")
            st.write(f"MoT Status: {vehicle_info.mot_status}")
            st.write(f"Colour: {vehicle_info.colour}")
            st.write(f"Year of Manufacture: {vehicle_info.year_of_manufacture}")
            st.write(f"Engine Capacity: {vehicle_info.capacity}")
            st.write(f"CO2 Emissions: {vehicle_info.co2_emissions}")

        # Initialize the trips and total_trip attributes for the vehicle object
        vehicle_info.trips = []
        vehicle_info.total_trip = TotalTrip()

        # Generate random trip data for the vehicle
        num_trips = random.randint(1, 3)
        for _ in range(num_trips):
            vehicle_info.generate_random_trip_data()

        # Generate random parking data for the vehicle
        vehicle_info.generate_random_parking_data()

        st.write(
            "Vehicles can be identified comprehensively from number plates i.e with cameras or sensors."
        )

        # -- Section: Vehicle History --
        st.header("📜 Vehicle History")
        st.subheader("Trip Data")
        st.write("This is information about the vehicle's trips.")

        with st.expander("Click to view trip data"):

            num_columns = min(num_trips, 3)
            trip_columns = st.columns(num_columns)

            for idx, trip in enumerate(vehicle_info.trips):
                with trip_columns[idx]:
                    st.write(f"Trip {idx+1}")  # fmt: skip
                    st.write(f"Roads: {', '.join(str(road) for road in trip.roads)}")  # fmt: skip
                    st.write(f"Locations: {', '.join(str(location) for location in trip.locations)}")  # fmt: skip
                    st.write(f"Stops: {str(trip.stops)}")  # fmt: skip
                    st.write(f"Mileage: {str(trip.mileage)}")  # fmt: skip
                    st.write(f"Trip Times:")  # fmt: skip
                    # for start_time, end_time in trip.trip_times: # fmt: skip
                    # st.write(f"  - Trip Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}") # fmt: skip
                    # st.write(f"  - Trip End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}") # fmt: skip
                    # st.write(f"Time in Traffic Jam: {str(trip.time_in_traffic_jam)} minutes")  # fmt: skip
                    st.write(f"Time on Freeway: {str(trip.time_on_freeway)} minutes")  # fmt: skip
                    # time_in_traffic_jam = timedelta(minutes=trip.time_in_traffic_jam)
                    # time_on_freeway = timedelta(minutes=trip.time_on_freeway)

                    # st.write(f"Time in Traffic Jam: {time_in_traffic_jam}")
                    # st.write(f"Time on Freeway: {time_on_freeway}")

        # st.write(f"Trip Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")  # fmt: skip

        st.subheader("Parking Data")
        st.write(
            "This is information about the vehicle's parking, such as parking time and parking locations. Vehicles are encouraged to park in silos or underground to reduce congestion"
        )
        with st.expander("Click to view parking data"):
            parking = vehicle_info.parking_data[-1]  # Get the latest parking data
            st.write(f"Location: {parking['location']}")
            st.write(f"Parking Type: {parking['parking_type']}")
            st.write(
                f"Entry Time: {parking['entry_time'].strftime('%Y-%m-%d %H:%M:%S')}"
            )
            st.write(f"Exit Time: {parking['exit_time'].strftime('%Y-%m-%d %H:%M:%S')}")

        # -- Section: Driver's Levy --
        st.header("🚦 Driver's Levy")
        st.subheader(
            "The Driver's Levy replaces the fuel levy and is calculated based on the vehicle's mileage and time spent on the road, (including differentiating between on highways and in traffic) It also bills drivers differently depending on engine displacement, fuel type and other trip data."
        )
        with st.expander("Click to calculate driver's levy"):
            num_columns = len(vehicle_info.trips)
            levy_columns = st.columns(num_columns)
            for idx, (trip, levy_column) in enumerate(
                zip(vehicle_info.trips, levy_columns)
            ):
                levy_info = generate_driver_levy_info(vehicle_info, trip)
                with levy_column:
                    st.write(f"Trip {idx + 1} Levy Info:")
                    st.write(f"Registration Number: {levy_info['registration_number']}")
                    st.write("Trip Data:")
                    st.write(f"Mileage: {levy_info['trip_data']['mileage']}")
                    st.write(f"Time in Traffic Jam:")
                    for start_time, end_time in levy_info["trip_data"][
                        "time_in_traffic_jam"
                    ]:
                        st.write(f"  - Start Time: {start_time}")
                        st.write(f"  - End Time: {end_time}")
                        st.write(
                            f"Time on Freeway: {levy_info['trip_data']['time_on_freeway']}"
                        )
                st.write(f"Driver's Levy Amount: ${levy_info['driver_levy_amount']}")

        # -- Section: Carbon Levy --
        st.header("🌳 Carbon Levy")
        st.subheader(
            "The Carbon Levy is calculated based on the vehicle's CO2 emissions rating, real driving emissions and other trip data. Discounts can be given if cars park underground or in silos, drive less or use electric cars."
        )
        with st.expander("Click to calculate carbon levy"):
            num_columns = len(vehicle_info.trips)
            levy_columns = st.columns(num_columns)
            for idx, (trip, levy_column) in enumerate(
                zip(vehicle_info.trips, levy_columns)
            ):
                levy_info = generate_carbon_levy_info(vehicle_info, trip)
                with levy_column:
                    st.write(f"Trip {idx + 1} Levy Info:")
                    st.write(f"Registration Number: {levy_info['registration_number']}")
                    st.write("Trip Data:")
                    st.write(f"Mileage: {levy_info['trip_data']['mileage']}")
                    st.write(f"Time in Traffic Jam:")
                    for start_time, end_time in levy_info["trip_data"][
                        "time_in_traffic_jam"
                    ]:
                        st.write(f"  - Start Time: {start_time}")
                        st.write(f"  - End Time: {end_time}")
                        st.write(
                            f"Time on Freeway: {levy_info['trip_data']['time_on_freeway']}"
                        )
                        st.write(
                            f"Carbon Levy Amount: ${levy_info['carbon_levy_amount']}"
                        )


# --- Section: Summary
st.header("📊 Summary")
# Summarize trip data
trip_summary = ", ".join(
    [
        f"Trip {idx + 1}: {trip.mileage} miles"
        for idx, trip in enumerate(vehicle_info.trips)
    ]
)

# Summarize parking data
latest_parking = vehicle_info.parking_data[-1]  # Get the latest parking data
parking_summary = f"Parking at {latest_parking['location']} ({latest_parking['parking_type']}) for {int((latest_parking['exit_time'] - latest_parking['entry_time']).total_seconds() / 60)} minutes"

# Calculate total levies
total_driver_levy = sum(
    generate_driver_levy_info(vehicle_info, trip)["driver_levy_amount"]
    for trip in vehicle_info.trips
)
total_carbon_levy = sum(
    generate_carbon_levy_info(vehicle_info, trip)["carbon_levy_amount"]
    for trip in vehicle_info.trips
)

# Construct the summary message
summary_message = (
    f"Vehicle {vehicle_info.registration_number} has completed {len(vehicle_info.trips)} trips recently.\n"
    f"The trips included {trip_summary}.\n{parking_summary}. "
    f"The total driver's levy for the trips amounts to {total_driver_levy:.2f}USD, and the total carbon levy is {total_carbon_levy:.2f}USD."
)

# Display the summary message
st.write(summary_message)

# -- Section: Billing

st.header("💰 Billing")
with st.expander("Billing"):
    st.write("Billing area. View and manage billing information here.")
    recipient = st.text_input("Enter your phone number", "+254712345678")
    message = summary_message
    # st.button("Send Bill")

    if st.button("Send Bill"):
        st.balloons()
        # Send a bill to the user's phone number

        SMS().send(message, [recipient])
        # recipients_message =
        st.write("Bill sent successfully!")

# -- Section: Chatbot
st.header("🤖 Chatbot")
with st.expander("[CLICK HERE TO OPEN CHATBOT]"):
    st.write("Welcome to URBAN & MOBILE AI Assistant. Ask about the software")
    test_user_string = st.text_input("💬")
    # OPENAI_API_KEY = st.secrets["openai_api_key"]

    # if api_key and test_user_string:
    if test_user_string:
        bot = Bot(
            # system="You are Jambo, the virtual assistant for Halisi. Halisi is a budding startup by undergraduate civil engineering students from the university of Nairobi, Kenya. Halisi prioritizes citizen-centric approaches and data-driven solutions across thematic areas like Public Health, Structures, Geotech, Water, and Transport. By collecting real-time data at the source and leveraging open-source software, we ensure efficient resource allocation and sustainable development, enhancing accountability and meeting evolving community needs",
            user=test_user_string,
            assistant="",
            # api=OPENAI_API_KEY,
            dataframe=summary_message,
        )

        response = bot.create_completion()
        st.write("URBAN & MOBILE AI Assistant:", response)
    else:
        st.warning(
            "This chatbot is for demonstration purposes only. Please enter a message to continue."
        )

# -- Section: Usable Map
st.header("🗺️ Usable Map")
with st.expander("Usable Map"):
    m = folium.Map(
        location=[-1.286389, 36.817223],
        zoom_start=5,
        min_lat=-1,
        max_lat=0,
        min_lon=36,
        max_lon=37,
        max_bounds=False,
        max_bounds_viscosity=1.0,
    )
    Draw(export=True).add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        # st.write(output)
        st.write(
            "Usable map area. See Nairobi, Kenya. You can find parking spots here with ease, including street parkings which are expensive, and silo parkings which are cheap"
        )
