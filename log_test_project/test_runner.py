fail = 0
passed = 0
heat_average = 0.0
with open("sensor_logs.txt", "r") as file:
	for line in file:
		parts = line.strip().split(",")
		time = parts[0]
		status = parts[1]
		voltage = float(parts[2])
		heat = float(parts[3])

		if status != "OK" or voltage < 3.3:
			fail += 1
		else:
			passed += 1
			heat_average += heat
		
		line_count = fail + passed
print ("Job Completed data count: ", line_count, "PASS: ", passed, "FAIL: ", fail, "Average heat: ", (heat_average / passed))
		
