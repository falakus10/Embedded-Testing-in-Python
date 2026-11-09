class SensorData:
	def __init__(self, ts: str, status: str, voltage: float, heat: float):
		self.time = ts
		self.st = status
		self.h = heat
		self.v = voltage

	def isValid(self) -> bool:
		return self.st == "OK" and self.v >= 3.3
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
    def __init__(self, sensor_list: list):
        self.sensor_list = sensor_list
        self.passed = 0
        self.failed = 0
        self.heat_average = 0.0
        self.line_count = 0

    def run(self):
        total_heat = 0.0
        for item in self.sensor_list:
            if item.isValid():
                self.passed += 1
                total_heat += item.h
            else:
                self.failed += 1
        
        self.line_count = self.passed + self.failed
        
        if self.passed > 0:
            self.heat_average = total_heat / self.passed
        else:
            self.heat_average = 0.0

    def generate_report(self):
        print(f"Job Completed | Total: {self.line_count} | PASS: {self.passed} | FAIL: {self.failed} | Avg Heat (PASS): {self.heat_average:.2f}°C")

parser = LogParser("sensor_logs.txt")
data_list = parser.parse_file()

runner = TestRunner(data_list)
runner.run()
runner.generate_report()