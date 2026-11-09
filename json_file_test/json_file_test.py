import json
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_execution.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("test")

with open("config.json", "r") as f:
	  config = json.load(f)

class SensorData:
	def __init__(self, ts: str, status: str, voltage: float, heat: float):
		self.time = ts
		self.st = status
		self.h = heat
		self.v = voltage

	def isValid(self, min_voltage: float, max_heat: float, allowed_statuses: list) -> bool:
			is_status_ok = self.st in allowed_statuses
			is_voltage_ok = self.v >= min_voltage
			is_heat_ok = self.h <= max_heat
	
			return is_status_ok and is_voltage_ok and is_heat_ok

class LogParser:
	def __init__(self, file_path: str):
		self.path = file_path

	def parse_file(self) -> list:
		with open(self.path, "r") as file:
			sensor_list = []
			for line in file:
				parts = line.strip().split(",")
				x = SensorData(parts[0], parts[1], float(parts[2]), float(parts[3]))
				sensor_list.append(x)
		return sensor_list

class TestRunner:
	def __init__(self, sensor_list: list, config: dict):
		self.sensor_list = sensor_list
		self.config = config
		self.passed = 0
		self.failed = 0
		self.heat_average = 0.0
		self.line_count = 0

	def run(self):
		total_heat = 0.0
		min_v = self.config["min_voltage"]
		max_h = self.config["max_heat"]
		statuses = self.config["allowed_statuses"]

		for item in self.sensor_list:
			if item.isValid(min_voltage=min_v, max_heat=max_h, allowed_statuses=statuses):
				self.passed += 1
				total_heat += item.h
			else:
				self.failed += 1
				logger.warning(f"FAIL -> Time: {item.time} | Status: {item.st} | V: {item.v}V | Heat: {item.h}°C")
		
		self.line_count = self.passed + self.failed
		
		if self.passed > 0:
			self.heat_average = total_heat / self.passed
		else:
			self.heat_average = 0.0

	def generate_report(self):
		logger.info(f"Job Completed | Total: {self.line_count} | PASS: {self.passed} | FAIL: {self.failed} | Avg Heat (PASS): {self.heat_average:.2f}°C")

parser = LogParser("sensor_logs.txt")
data_list = parser.parse_file()

runner = TestRunner(data_list, config)
runner.run()
runner.generate_report()