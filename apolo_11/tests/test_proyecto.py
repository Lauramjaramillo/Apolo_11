import os
import json
from apolo_11.Proyecto import ConfigLoader, DataGenerator
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Rutas para las pruebas
CONFIG_PATH = "tests/test_config.json"
DEVICES_FOLDER_TEST = "devices_test"

def test_config_loader():
    """
    Test para la clase ConfigLoader.

    Verifica que la carga de la configuración desde un archivo JSON funciona correctamente.
    """
    config_data = {
        "output_path": f"./{DEVICES_FOLDER_TEST}",
        "devices": ["dispositivo1", "dispositivo2"],
        "missions": {"mision1": "M1", "mision2": "M2"},
        "statuses": ["estado1", "estado2"],
        "time_sleep": 10,
        "num_files_range": [5, 10]
    }

    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

    config_loader = ConfigLoader(CONFIG_PATH)

    assert config_loader.output_path == f"./{DEVICES_FOLDER_TEST}"
    assert config_loader.devices == ["dispositivo1", "dispositivo2"]
    assert config_loader.missions == {"mision1": "M1", "mision2": "M2"}
    assert config_loader.statuses == ["estado1", "estado2"]
    assert config_loader.time_sleep == 10
    assert config_loader.num_files_range == [5, 10]

def test_data_generator():
    """
    Test para la clase DataGenerator.

    Verifica que la generación de archivos simulados funciona correctamente.
    """
    config_data = {
        "output_path": f"./{DEVICES_FOLDER_TEST}",
        "devices": ["dispositivo1", "dispositivo2"],
        "missions": {"mision1": "M1", "mision2": "M2"},
        "statuses": ["estado1", "estado2"],
        "time_sleep": 10,
        "num_files_range": [5, 10]
    }

    with open(CONFIG_PATH, 'w') as config_file:
        json.dump(config_data, config_file)

    config_loader = ConfigLoader(CONFIG_PATH)
    data_generator = DataGenerator(config_loader)

    iteration_count = 1
    data_generator.generate_files(iteration_count)
