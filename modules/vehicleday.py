from datetime import datetime, timedelta  # FIXME: fix rendering, consider Ruby strftime https://apidock.com/ruby/DateTime/strftime # fmt: skip


class Trip:
    def __init__(
        self,
        roads,
        locations,
        stops,
        capacity,
        trip_times,
        time_in_traffic_jam,
        time_on_freeway,
        mileage,
    ):
        self.roads = roads
        self.locations = locations
        self.stops = stops
        self.capacity = capacity
        self.trip_times = trip_times
        self.time_in_traffic_jam = time_in_traffic_jam
        self.time_on_freeway = time_on_freeway
        self.mileage = mileage


class TotalTrip:
    def __init__(self):
        self.trips = []

    def add_trip(self, trip):
        self.trips.append(trip)

    def get_total_capacity(self):
        return sum([trip.capacity for trip in self.trips])

    def get_total_trip_time(self):
        return sum(
            [
                sum((end - start).seconds // 60 for start, end in trip.trip_times)
                for trip in self.trips
            ]
        )

    def get_total_time_in_traffic_jam(self):
        return sum([trip.time_in_traffic_jam for trip in self.trips])

    def get_total_time_on_freeway(self):
        return sum([trip.time_on_freeway for trip in self.trips])


class Parking:
    def __init__(self, location, parking_type, time_spent):
        self.location = location
        self.parking_type = parking_type  # on_street, underground, or in_silo
        self.time_spent = time_spent
