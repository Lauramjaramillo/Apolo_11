from typing import List, Dict, Union
import os
import json
import pandas as pd
import logging
from datetime import datetime
from functools import wraps  # Importa wraps del modulo functools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} ejecutado en {execution_time.total_seconds():.2f} segundos.")
        return result
    return wrapper


class ReportGenerator:
    """
    Clase para generar informes a partir de archivos generados.

    Attributes:
        devices_folder (str): Ruta a la carpeta donde se encuentran los archivos generados.
        reports_folder (str): Ruta a la carpeta donde se guardaran los informes.
    """

    def __init__(self, devices_folder: str, reports_folder: str) -> None:
        """
        Inicializa una instancia de ReportGenerator.

        Parameters:
            devices_folder (str): Ruta a la carpeta donde se encuentran los archivos generados.
            reports_folder (str): Ruta a la carpeta donde se guardaran los informes.
        """
        self.devices_folder = devices_folder
        self.reports_folder = reports_folder

    def generate_analysis_reports(self) -> None:
        """
        Genera informes para cada subdirectorio en la carpeta de dispositivos.

        Returns:
            None
        """
        for folder_name in os.listdir(self.devices_folder):
            folder_path = os.path.join(self.devices_folder, folder_name)
            if os.path.isdir(folder_path):
                data = self.load_data(folder_path)
                df = pd.DataFrame(data)
                self.generate_report(folder_name, df)

    def load_data(self, folder_path: str) -> List[Dict[str, Union[str, int]]]:
        """
        Carga los datos de archivos en un subdirectorio.

        Parameters:
            folder_path (str): Ruta al subdirectorio.

        Returns:
            List[Dict[str, Union[str, int]]]: Datos cargados desde los archivos.
        """
        data = []
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r') as file:
                    file_data = json.load(file)
                    data.append(file_data)
        return data

    @timing_decorator  # Aplica el decorador
    def generate_report(self, folder_name: str, df: pd.DataFrame) -> None:
        """
        Genera un informe para un subdirectorio.

        Parameters:
            folder_name (str): Nombre del subdirectorio.
            df (pd.DataFrame): DataFrame de datos.

        Returns:
            None
        """
        report_filename = f"APLSTATS-REPORT[{folder_name}]-{datetime.now().strftime('%d%m%y%H%M%S')}.log"
        report_path = os.path.join(self.reports_folder, report_filename)

        try:
            with open(report_path, 'w') as report_file:
                report_file.write(self.analyze_events(df))
                report_file.write(self.detect_disconnections(df))
                report_file.write(self.consolidate_missions(df))
                report_file.write(self.calculate_percentages(df))

            logger.info(f"Reporte generado exitosamente en: {report_path}")

        except Exception as e:
            logger.error(f"Error al generar el reporte: {str(e)}")

    def analyze_events(self, df: pd.DataFrame) -> str:
        """
        Realiza un analisis de eventos y devuelve el resultado como una cadena.

        Parameters:
            df (pd.DataFrame): DataFrame de datos.

        Returns:
            str: Resultado del analisis de eventos.
        """
        events_analysis = "\n\nb) Analisis de eventos\n"
        events_analysis += df.groupby(['mission', 'device_type', 'device_status']).size().unstack().to_string()
        return events_analysis

    def detect_disconnections(self, df: pd.DataFrame) -> str:
        """
        Identifica las desconexiones y devuelve el resultado como una cadena.

        Parameters:
            df (pd.DataFrame): DataFrame de datos.

        Returns:
            str: Resultado de la identificacion de desconexiones.
        """
        disconnections_analysis = "\n\nc) Gestion de desconexiones\n"
        unknown_disconnections = df[df['device_status'] == 'unknown'].groupby(['mission', 'device_type']).size().unstack()
        disconnections_analysis += unknown_disconnections.to_string()
        return disconnections_analysis

    def consolidate_missions(self, df: pd.DataFrame) -> str:
        """
        Consolida las misiones y devuelve el resultado como una cadena.

        Parameters:
            df (pd.DataFrame): DataFrame de datos.

        Returns:
            str: Resultado de la consolidacion de misiones.
        """
        consolidation_analysis = "\n\nd) Consolidacion de misiones\n"
        inoperable_devices = df[df['device_status'].isin(['faulty', 'killed', 'unknown'])].groupby(['mission']).size()
        consolidation_analysis += inoperable_devices.to_string()
        return consolidation_analysis

    def calculate_percentages(self, df: pd.DataFrame) -> str:
        """
        Calcula los porcentajes y devuelve el resultado como una cadena.

        Parameters:
            df (pd.DataFrame): DataFrame de datos.

        Returns:
            str: Resultado del calculo de porcentajes.
        """
        percentages_analysis = "\n\ne) Calculo de porcentajes\n"
        total_data = len(df)
        device_mission_percentages = (df.groupby(['mission', 'device_type']).size() / total_data * 100).unstack()
        percentages_analysis += device_mission_percentages.to_string()
        return percentages_analysis

    def move_devices_to_backup(self) -> None:
        """
        Mueve todas las subcarpetas de la carpeta 'devices' a la carpeta 'backups'.
        """
        devices_backup_folder = os.path.join("backups")

        try:
            os.makedirs(devices_backup_folder, exist_ok=True)

            for subfolder_name in os.listdir(self.devices_folder):
                subfolder_path = os.path.join(self.devices_folder, subfolder_name)
                if os.path.isdir(subfolder_path):
                    os.replace(subfolder_path, os.path.join(devices_backup_folder, subfolder_name))

            logger.info("Subcarpetas de 'devices' movidas a 'backups' exitosamente.")
        except Exception as e:
            logger.error(f"Error al mover las subcarpetas a 'backups': {str(e)}")

    @staticmethod
    def run_reporte(reporte_path: str) -> None:
        try:
            devices_folder = "devices"
            reports_folder = "reports"

            os.makedirs("backups", exist_ok=True)
            os.makedirs(reports_folder, exist_ok=True)

            report_generator = ReportGenerator(devices_folder, reports_folder)
            report_generator.generate_analysis_reports()
            report_generator.move_devices_to_backup()

        except Exception as e:
            logger.error(f"Error inesperado en el programa: {str(e)}")
