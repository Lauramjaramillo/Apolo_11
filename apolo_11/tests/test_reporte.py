import os
import pytest
import pandas as pd
from apolo_11.Reporte import ReportGenerator

# Rutas para las pruebas
REPORTS_FOLDER_TEST = os.path.join("reports_test")
DEVICES_FOLDER_TEST = "devices_test"

# Fixture para inicializar la instancia de ReportGenerator
@pytest.fixture
def report_generator():
    return ReportGenerator(DEVICES_FOLDER_TEST, REPORTS_FOLDER_TEST)

# Prueba para asegurarse de que se puedan cargar datos desde un subdirectorio
def test_load_data(report_generator):
    # Crear algunos datos de prueba en DEVICES_FOLDER_TEST antes de ejecutar esta prueba
    data = report_generator.load_data(DEVICES_FOLDER_TEST)
    assert isinstance(data, list)

# Prueba para verificar que se pueda generar un informe sin errores
def test_generate_report(report_generator):
    # Crear algunos datos de prueba en DEVICES_FOLDER_TEST antes de ejecutar esta prueba
    data = report_generator.load_data(DEVICES_FOLDER_TEST)
    df = pd.DataFrame(data)
    
    # Asegúrate de que la carpeta de informes de prueba exista
    os.makedirs(REPORTS_FOLDER_TEST, exist_ok=True)

    # Ejecutar la prueba
    report_generator.generate_report("test_folder", df)

    # Asegurarse de que se haya generado un informe en la carpeta de informes de prueba
    assert os.path.exists(os.path.join(REPORTS_FOLDER_TEST, "APLSTATS-REPORT[test_folder].log"))

# Prueba para verificar que se puedan mover los dispositivos a la carpeta de respaldo
def test_move_devices_to_backup(report_generator):
    # Crear algunos datos de prueba en DEVICES_FOLDER_TEST antes de ejecutar esta prueba

    # Asegúrate de que la carpeta de respaldo exista
    os.makedirs("backups_test", exist_ok=True)

    # Ejecutar la prueba
    report_generator.move_devices_to_backup()

    # Asegurarse de que las subcarpetas de dispositivos estén en la carpeta de respaldo
    assert os.path.exists(os.path.join("backups_test", "test_folder"))
