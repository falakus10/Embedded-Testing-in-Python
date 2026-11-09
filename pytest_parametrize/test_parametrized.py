import pytest
from sensor_models import SensorData

@pytest.fixture
def sample_config():
    return {
        "min_voltage": 3.3,
        "max_heat": 60.0,
        "allowed_statuses": ["OK"]
    }


@pytest.mark.parametrize(
    "voltage, expected_result",
    [
        (3.7, True),
        (3.3, True),
        (3.29, False),
        (2.5, False)
    ]
)
def test_voltage_boundary(sample_config, voltage, expected_result):

    data = SensorData(ts="2026-11-09T14:00:00", status="OK", voltage=voltage, heat=45.0)
    
    result = data.isValid(
        min_voltage=sample_config["min_voltage"],
        max_heat=sample_config["max_heat"],
        allowed_statuses=sample_config["allowed_statuses"]
    )
    
    assert result == expected_result


@pytest.mark.parametrize(
    "status, voltage, heat, expected_result",
    [
        ("OK", 3.8, 45.0, True),
        ("ERR_CRC", 3.8, 45.0, False),
        ("OK", 3.8, 70.0, False),
        ("ERR_TIMEOUT", 3.0, 65.0, False)
    ]
)
def test_sensor_combinations(sample_config, status, voltage, heat, expected_result):
    data = SensorData(ts="2026-11-09T14:00:00", status=status, voltage=voltage, heat=heat)
    
    result = data.isValid(
        min_voltage=sample_config["min_voltage"],
        max_heat=sample_config["max_heat"],
        allowed_statuses=sample_config["allowed_statuses"]
    )
    
    assert result == expected_result