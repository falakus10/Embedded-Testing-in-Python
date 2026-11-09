import pytest
from sensor_models import SensorData, LogParser

@pytest.fixture
def sample_config():
	return {
		"min_voltage" : 3.3,
		"max_heat" : 60,
		"allowed_status" : ["OK"] 
	}

@pytest.fixture
def valid_sensor_data():
	data = SensorData("2026-11-09T14:00:00", "OK", 3.5, 43.3)
	return data

def test_low_voltage_fail(valid_sensor_data, sample_config):

	valid_sensor_data.v = 3.0
	result = valid_sensor_data.isValid(
		min_voltage=sample_config["min_voltage"],
		max_heat=sample_config["max_heat"],
		allowed_statuses=sample_config["allowed_status"]
	)
	
	assert result == False

def test_high_heat_fail(valid_sensor_data, sample_config):

	valid_sensor_data.h = 70.0
	result = valid_sensor_data.isValid(
		min_voltage=sample_config["min_voltage"],
		max_heat=sample_config["max_heat"],
		allowed_statuses=sample_config["allowed_status"]
	)

	assert result == False

def test_invalid_status_fail(valid_sensor_data, sample_config):

	valid_sensor_data.st = "ERR_CRC"
	result = valid_sensor_data.isValid(
		min_voltage=sample_config["min_voltage"],
		max_heat=sample_config["max_heat"],
		allowed_statuses=sample_config["allowed_status"]
	)
	assert result == False

def test_corrupted_log_parser():
	parser = LogParser("corrupted_logs.txt")
	with pytest.raises(ValueError):
		parser.parse_file()
