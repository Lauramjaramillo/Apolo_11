from typing import List, Dict, Union
import os
import random
import json
from datetime import datetime
import time
import uuid
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigLoader:
    """
    Clase para cargar la configuración desde un archivo JSON.

    Attributes:
        __output_path (str): Ruta predeterminada para la salida.
        __devices (List[str]): Lista de tipos de dispositivos.
        __missions (Dict[str, str]): Diccionario de misiones con sus abreviaturas.
        __statuses (List[str]): Lista de estados posibles para los dispositivos.
        __time_sleep (int): Tiempo de espera predeterminado.
        __num_files_range (List[int]): Rango para generar el número de archivos.
    """

    def __init__(self, config_path: str) -> None:
        """
        Inicializa una instancia de ConfigLoader.

        Parameters:
            config_path (str): Ruta al archivo de configuración (config.json).
        """
        self.__load_config(config_path)

    def __load_config(self, config_path: str) -> None:
        """
        Carga la configuración desde un archivo JSON.

        Parameters:
            config_path (str): Ruta al archivo de configuración (config.json).

        Returns:
            None
        """
        try:
            with open(config_path, 'r') as config_file:
                config_data = json.load(config_file)

            self.__output_path: str = config_data.get('output_path', './devices')
            self.__devices: List[str] = config_data.get('devices', [])
            self.__missions: Dict[str, str] = config_data.get('missions', {})
            self.__statuses: List[str] = config_data.get('statuses', ['excellent', 'good', 'warning', 'faulty', 'killed', 'unknown'])
            self.__time_sleep: int = config_data.get('time_sleep', 20)
            self.__num_files_range: List[int] = config_data.get('num_files_range', [1, 100])

            logging.info("Configuración cargada correctamente.")

        except FileNotFoundError:
            logging.error(f"Error: Archivo de configuración no encontrado en la ruta {config_path}.")
            exit(1)
        except json.JSONDecodeError:
            logging.error("Error: El archivo de configuración no es válido JSON.")
            exit(1)
        except Exception as e:
            logging.error(f"Error desconocido al cargar la configuración: {str(e)}")
            exit(1)

    @property
    def output_path(self) -> str:
        """
        Obtiene la ruta de salida.

        Returns:
            str: Ruta de salida.
        """
        return self.__output_path

    @property
    def devices(self) -> List[str]:
        """
        Obtiene la lista de tipos de dispositivos.

        Returns:
            List[str]: Lista de tipos de dispositivos.
        """
        return self.__devices

    @property
    def missions(self) -> Dict[str, str]:
        """
        Obtiene el diccionario de misiones con sus abreviaturas.

        Returns:
            Dict[str, str]: Diccionario de misiones.
        """
        return self.__missions

    @property
    def statuses(self) -> List[str]:
        """
        Obtiene la lista de estados posibles para los dispositivos.

        Returns:
            List[str]: Lista de estados posibles.
        """
        return self.__statuses

    @property
    def time_sleep(self) -> int:
        """
        Obtiene el tiempo de espera predeterminado.

        Returns:
            int: Tiempo de espera predeterminado.
        """
        return self.__time_sleep

    @property
    def num_files_range(self) -> List[int]:
        """
        Obtiene el rango para generar el número de archivos.

        Returns:
            List[int]: Rango para el número de archivos.
        """
        return self.__num_files_range

    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la instancia de ConfigLoader.

        Returns:
            str: Representación en cadena.
        """
        return (
            f"ConfigLoader instance:\n"
            f"  Output Path: {self.output_path}\n"
            f"  Devices: {self.devices}\n"
            f"  Missions: {self.missions}\n"
            f"  Statuses: {self.statuses}\n"
            f"  Time Sleep: {self.time_sleep}\n"
            f"  Num Files Range: {self.num_files_range}\n"
        )


class DataGenerator:
    """
    Clase para generar datos y archivos simulados.

    Attributes:
        __config_loader (ConfigLoader): Instancia de ConfigLoader que proporciona la configuración.
    """

    def __init__(self, config_loader: ConfigLoader) -> None:
        """
        Inicializa una instancia de DataGenerator.

        Parameters:
            config_loader (ConfigLoader): Instancia de ConfigLoader que proporciona la configuración.
        """
        self.__config_loader: ConfigLoader = config_loader

    @classmethod
    def from_config_path(cls, config_path: str) -> 'DataGenerator':
        """
        Método de clase para inicializar una instancia de DataGenerator a partir de un archivo de configuración.

        Parameters:
            config_path (str): Ruta al archivo de configuración (config.json).

        Returns:
            DataGenerator: Instancia de DataGenerator.
        """
        config_loader = ConfigLoader(config_path)
        return cls(config_loader)

    def generate_random_status(self) -> str:
        """
        Genera un estado aleatorio para un dispositivo.

        Returns:
            str: Estado aleatorio.
        """
        return random.choice(self.__config_loader.statuses)

    def generate_hash(self, data: Dict[str, Union[str, int]]) -> str:
        """
        Genera el hash SHA-256 de un diccionario convertido a cadena JSON.

        Parameters:
            data (Dict[str, Union[str, int]]): Datos a ser hashados.

        Returns:
            str: Hash SHA-256.
        """
        hash_object = hashlib.sha256(json.dumps(data).encode())
        return hash_object.hexdigest()

    def generate_file_data(self, mission: str, unique_id: str) -> Dict[str, Union[str, int]]:
        """
        Genera datos simulados para un archivo.

        Parameters:
            mission (str): Misión asociada a los datos.
            unique_id (str): Identificador único para misiones desconocidas.

        Returns:
            Dict[str, Union[str, int]]: Datos simulados para el archivo.
        """
        device = random.choice(self.__config_loader.devices)
        data: Dict[str, Union[str, int]] = {
            "date": datetime.now().isoformat(),
            "mission": mission,
            "device_type": device,
            "device_status": self.generate_random_status(),
            "hash": ""
        }

        if mission == 'Unknown':
            data['mission'] = unique_id
            data['device_type'] = 'unknown'
            data['device_status'] = 'unknown'

        return data

    def generate_files(self, iteration_count: int) -> None:
        """
        Genera archivos simulados en una carpeta.

        Parameters:
            iteration_count (int): Contador de iteraciones.

        Returns:
            None
        """
        try:
            num_files = random.randint(self.__config_loader.num_files_range[0], self.__config_loader.num_files_range[1])

            folder_name = f"{iteration_count}_{num_files}"
            folder_path = os.path.join(self.__config_loader.output_path, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            unique_id = str(uuid.uuid4())

            for i in range(1, num_files + 1):
                mission = random.choice(list(self.__config_loader.missions.keys()))

                file_name = f"APL{self.__config_loader.missions[mission]}-0000{i}.log"
                file_path = os.path.join(folder_path, file_name)

                data = self.generate_file_data(mission, unique_id)

                if not file_name.startswith("APLUNKN"):
                    data['hash'] = self.generate_hash(data)

                with open(file_path, 'w') as file:
                    json.dump(data, file, indent=4)

                logging.info(f"Archivo {file_name} generado en {folder_name} con éxito.")

            time.sleep(self.__config_loader.time_sleep)

        except OSError as e:
            logger.error(f"Error al crear directorio o archivo: {str(e)}")
        except Exception as e:
            logger.error(f"Error desconocido al generar archivos: {str(e)}")

        # Se mueve la lógica de eliminación del directorio fuera del bloque try-except
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                try:
                    with open(os.path.join(root, file), 'r'):
                        pass
                except Exception as e:
                    logger.error(f"Error al cerrar el archivo: {str(e)}")

        try:
            os.removedirs(folder_path)
        except OSError as e:
            logger.error(f"Error al eliminar directorio: {str(e)}")

    @staticmethod
    def run_proyecto(config_path: str, proyecto_path: str) -> None:
        config_loader = ConfigLoader(config_path)
        data_generator = DataGenerator(config_loader)

        iteration_count = 0
        while True:
            iteration_count += 1
            data_generator.generate_files(iteration_count)


if __name__ == "__main__":
    DataGenerator.run_proyecto()
