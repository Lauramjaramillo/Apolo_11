import os
import argparse
from Proyecto import DataGenerator, ConfigLoader
from Reporte import ReportGenerator


def main():
    """
    Función principal para ejecutar Proyecto.py o Reporte.py en el contexto de Apolo_11.

    Esta función maneja la entrada del usuario y ejecuta el script correspondiente (Proyecto o Reporte).
    """
    parser = argparse.ArgumentParser(description="Ejecutar Proyecto.py o Reporte.py en el contexto de Apolo_11.")
    parser.add_argument("script", choices=["proyecto", "reporte"], help="Selecciona 'proyecto' o 'reporte'.")
    args = parser.parse_args()

    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "config.json")
    proyecto_path = os.path.join(base_path, "Proyecto.py")

    if args.script == "proyecto":
        # Ejecutar Proyecto
        config_loader = ConfigLoader(config_path)
        data_generator = DataGenerator(config_loader)
        data_generator.run_proyecto(config_path, proyecto_path)
    elif args.script == "reporte":
        # Ejecutar Reporte
        ReportGenerator.run_reporte(config_path)


if __name__ == "__main__":
    main()
