class SimData:
    _instances = {}  # Dictionary to store SimData instances with call_sign as keys

    def __new__(cls, call_sign, *args, **kwargs):
        # Check if a SimData instance with the same call_sign already exists
        if call_sign in cls._instances:
            raise ValueError(f"A SimData object with call_sign '{call_sign}' already exists.")
        
        # If not, create a new SimData instance
        instance = super().__new__(cls)
        cls._instances[call_sign] = instance
        return instance

    def __init__(self, call_sign, aircraft_type, liveries, sim_time, latitude, longitude, current_altitude,
                 heading, roll, pitch, ground_speed, is_on_the_ground, ils_in_range, maneuver, emergency_flag,
                 airport_altitude, lamp_flag):
        if not hasattr(self, 'initialized'):
            self.call_sign = call_sign
            self.aircraft_type = aircraft_type
            self.liveries = liveries
            self.sim_time = sim_time
            self.latitude = latitude
            self.longitude = longitude
            self.current_altitude = current_altitude
            self.heading = heading
            self.roll = roll
            self.pitch = pitch
            self.ground_speed = ground_speed
            self.is_on_the_ground = is_on_the_ground
            self.ils_in_range = ils_in_range
            self.maneuver = maneuver
            self.emergency_flag = emergency_flag
            self.airport_altitude = airport_altitude
            self.lamp_flag = lamp_flag
            self.initialized = True

    def update(self, aircraft_type, liveries, sim_time, latitude, longitude, current_altitude,
               heading, roll, pitch, ground_speed, is_on_the_ground, ils_in_range, maneuver, emergency_flag,
               airport_altitude, lamp_flag):
        self.aircraft_type = aircraft_type
        self.liveries = liveries
        self.sim_time = sim_time
        self.latitude = latitude
        self.longitude = longitude
        self.current_altitude = current_altitude
        self.heading = heading
        self.roll = roll
        self.pitch = pitch
        self.ground_speed = ground_speed
        self.is_on_the_ground = is_on_the_ground
        self.ils_in_range = ils_in_range
        self.maneuver = maneuver
        self.emergency_flag = emergency_flag
        self.airport_altitude = airport_altitude
        self.lamp_flag = lamp_flag

    def to_dict(self):
        return {
            "call_sign": self.call_sign,
            "aircraft_type": self.aircraft_type,
            "liveries": self.liveries,
            "sim_time": self.sim_time,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "current_altitude": self.current_altitude,
            "heading": self.heading,
            "roll": self.roll,
            "pitch": self.pitch,
            "ground_speed": self.ground_speed,
            "is_on_the_ground": self.is_on_the_ground,
            "ils_in_range": self.ils_in_range,
            "maneuver": self.maneuver,
            "emergency_flag": self.emergency_flag,
            "airport_altitude": self.airport_altitude,
            "lamp_flag": self.lamp_flag
        }
