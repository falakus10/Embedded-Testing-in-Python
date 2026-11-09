import random
from datetime import datetime


print(random.random())
dev_id = "DEV_01"

with open("sensor_logs.txt", "a")as file:
	for i in range(20):
		ts = datetime.now().isoformat()
		voltage = round(random.uniform(3.0, 4.2), 2)
		heat = round(random.uniform(20.0, 65.0), 2)
		status = random.choice(["OK", "OK", "OK", "ERR_CRC"])
		line = f"{ts},{status},{voltage},{heat}\n"
		file.write(line)

print("20 line log written in file")


