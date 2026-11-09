# sensor_models.py

class SensorData:
    def __init__(self, ts: str, status: str, voltage: float, heat: float):
        self.time = ts
        self.st = status
        self.v = voltage
        self.h = heat

    def isValid(self, min_voltage: float, max_heat: float, allowed_statuses: list) -> bool:
        is_status_ok = self.st in allowed_statuses
        is_voltage_ok = self.v >= min_voltage
        is_heat_ok = self.h <= max_heat

        return is_status_ok and is_voltage_ok and is_heat_ok

# sensor_models.py içinde olmalı

class LogParser:
    def __init__(self, file_path: str):
        self.path = file_path

    def parse_file(self) -> list:
        sensor_list = []
        with open(self.path, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                x = SensorData(parts[0], parts[1], float(parts[2]), float(parts[3]))
                sensor_list.append(x)
        return sensor_list


