# test_sensor_pipeline.py

from sensor_models import SensorData, LogParser

# Testlerde baz alacağımız sınır konfigürasyon
TEST_CONFIG = {
	"min_voltage": 3.3,
	"max_heat": 60.0,
	"allowed_statuses": ["OK"]
}

def test_valid_sensor_data():
	data = SensorData(ts="2026-11-09T14:00:00", status="OK", voltage=3.7, heat=45.0)
	
	result = data.isValid(
		min_voltage=TEST_CONFIG["min_voltage"],
		max_heat=TEST_CONFIG["max_heat"],
		allowed_statuses=TEST_CONFIG["allowed_statuses"]
	)
	
	assert result == True

def test_low_voltage_fail():
	data = SensorData(ts="2026-11-09T14:00:00", status="OK", voltage=3.0, heat=45.0)
	
	result = data.isValid(
		min_voltage=TEST_CONFIG["min_voltage"],
		max_heat=TEST_CONFIG["max_heat"],
		allowed_statuses=TEST_CONFIG["allowed_statuses"]
	)
	
	assert result == False

def test_high_heat_fail():
	data = SensorData(ts="2026-11-09T14:00:00", status="OK", voltage=3.7, heat=70.0)

	result = data.isValid(
		min_voltage=TEST_CONFIG["min_voltage"],
		max_heat=TEST_CONFIG["max_heat"],
		allowed_statuses=TEST_CONFIG["allowed_statuses"]
	)

	assert result == False

def test_invalid_status_fail():
	data = SensorData(ts="2026-11-09T14:00:00", status="ERR_CRC", voltage=3.7, heat=30.0)

	result = data.isValid(
		min_voltage=TEST_CONFIG["min_voltage"],
		max_heat=TEST_CONFIG["max_heat"],
		allowed_statuses=TEST_CONFIG["allowed_statuses"]
	)

	assert result == False

def test_full_log_file_integration():
    # 1. LogParser ile 20 satırlık dosyayı okuyoruz
    parser = LogParser("sensor_logs.txt")
    data_list = parser.parse_file()
    
    # 2. Dosyada gerçekten 20 satır veri var mı kontrolü
    assert len(data_list) == 60
    
    # 3. Her bir sensör verisini sırayla dönüp tipleri ve sınırları doğruluyoruz
    for data in data_list:
        assert isinstance(data.v, float)
        assert isinstance(data.h, float)
        # Voltaj 3.0V ile 4.2V arasında mı?
        assert 3.0 <= data.v <= 4.2
        # Sıcaklık 20.0°C ile 65.0°C arasında mı?
        assert 20.0 <= data.h <= 65.0


