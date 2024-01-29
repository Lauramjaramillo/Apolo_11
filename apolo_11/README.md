# Proyecto Apolo-11: Sistema de Monitoreo para Misiones Espaciales de la NASA

La Administración Nacional de la Aeronáutica y el Espacio, más conocida como NASA (National Aeronautics and Space Administration), está inmersa en un período de revitalización y ambición, buscando recuperar su posición destacada en la exploración espacial. Actualmente, la NASA está llevando a cabo cuatro proyectos de vanguardia en su historia:

1. **OrbitOne:** Modernizar la flota de satélites para mejorar el rendimiento, la cobertura y las comunicaciones.

2. **ColonyMoon:** Establecer una colonia en la Luna.

3. **VacMars:** Realizar viajes turísticos a Marte.

4. **GalaxyTwo:** Explorar la posibilidad de visitar otras galaxias.

Estos proyectos, impulsados por tecnologías innovadoras, generan una expectación mundial. La NASA reconoce la importancia crítica de gestionar anomalías para garantizar el éxito de las misiones.

Para abordar este desafío, la NASA está implementando un sistema de monitoreo unificado basado en la transmisión de archivos a intervalos de 20 segundos. Este sistema permitirá un control detallado de satélites, naves y vehículos espaciales, facilitando acciones preventivas y garantizando la seguridad de astronautas y turistas.

Como uno de los ingenieros jefe más experimentados, se le convoca para liderar la simulación inicial de este sistema, denominado "Apolo-11". Este programa es crucial para la consolidación y monitoreo de registros generados por diversos componentes, como satélites, naves, trajes y vehículos espaciales. Operado manualmente por el comandante, su contribución desempeñará un papel fundamental en el éxito de estas trascendentales iniciativas científicas y exploratorias.

## Contenido del Repositorio

- [Proyecto.py](#proyecto)
- [Reporte.py](#reporte)
- [Apolo_11.py](#apolo_11)

# Proyecto.py

Este módulo contiene las clases y funciones necesarias para simular la generación de datos y archivos en un proyecto ficticio.

## ConfigLoader

La clase `ConfigLoader` se encarga de cargar la configuración desde un archivo JSON.

### Atributos:

- `__output_path (str)`: Ruta predeterminada para la salida.
- `__devices (List[str])`: Lista de tipos de dispositivos.
- `__missions (Dict[str, str])`: Diccionario de misiones con sus abreviaturas.
- `__statuses (List[str])`: Lista de estados posibles para los dispositivos.
- `__time_sleep (int)`: Tiempo de espera predeterminado.
- `__num_files_range (List[int])`: Rango para generar el número de archivos.

### Métodos:

- `__init__(self, config_path: str) -> None`: Inicializa una instancia de ConfigLoader.
- `__load_config(self, config_path: str) -> None`: Carga la configuración desde un archivo JSON.
- `output_path(self) -> str`: Obtiene la ruta de salida.
- `devices(self) -> List[str]`: Obtiene la lista de tipos de dispositivos.
- `missions(self) -> Dict[str, str]`: Obtiene el diccionario de misiones con sus abreviaturas.
- `statuses(self) -> List[str]`: Obtiene la lista de estados posibles para los dispositivos.
- `time_sleep(self) -> int`: Obtiene el tiempo de espera predeterminado.
- `num_files_range(self) -> List[int]`: Obtiene el rango para generar el número de archivos.
- `__str__(self) -> str`: Devuelve una representación en cadena de la instancia de ConfigLoader.

## DataGenerator

La clase `DataGenerator` se encarga de generar datos y archivos simulados.

### Atributos:

- `__config_loader (ConfigLoader)`: Instancia de ConfigLoader que proporciona la configuración.

### Métodos:

- `__init__(self, config_loader: ConfigLoader) -> None`: Inicializa una instancia de DataGenerator.
- `from_config_path(cls, config_path: str) -> 'DataGenerator'`: Método de clase para inicializar una instancia de DataGenerator a partir de un archivo de configuración.
- `generate_random_status(self) -> str`: Genera un estado aleatorio para un dispositivo.
- `generate_hash(self, data: Dict[str, Union[str, int]]) -> str`: Genera el hash SHA-256 de un diccionario convertido a cadena JSON.
- `generate_file_data(self, mission: str, unique_id: str) -> Dict[str, Union[str, int]]`: Genera datos simulados para un archivo.
- `generate_files(self, iteration_count: int) -> None`: Genera archivos simulados en una carpeta.
- `run_proyecto(config_path: str, proyecto_path: str) -> None`: Método estático para ejecutar el proyecto.

## Ejecución del Proyecto

Antes de ejecutar el proyecto, asegúrate de tener las dependencias instaladas. Puedes hacerlo utilizando [Poetry](https://python-poetry.org/):

```bash
poetry install

```

# Reporte.py

Este módulo contiene la clase `ReportGenerator` que se encarga de generar informes a partir de archivos generados.

## ReportGenerator

La clase `ReportGenerator` tiene la funcionalidad de analizar los datos generados y generar informes con estadísticas relevantes.

### Atributos:

- `devices_folder (str)`: Ruta a la carpeta donde se encuentran los archivos generados.
- `reports_folder (str)`: Ruta a la carpeta donde se guardarán los informes.

### Métodos:

- `__init__(self, devices_folder: str, reports_folder: str) -> None`: Inicializa una instancia de ReportGenerator.
- `generate_analysis_reports(self) -> None`: Genera informes para cada subdirectorio en la carpeta de dispositivos.
- `load_data(self, folder_path: str) -> List[Dict[str, Union[str, int]]]`: Carga los datos de archivos en un subdirectorio.
- `generate_report(self, folder_name: str, df: pd.DataFrame) -> None`: Genera un informe para un subdirectorio.
- `analyze_events(self, df: pd.DataFrame) -> str`: Realiza un análisis de eventos y devuelve el resultado como una cadena.
- `detect_disconnections(self, df: pd.DataFrame) -> str`: Identifica las desconexiones y devuelve el resultado como una cadena.
- `consolidate_missions(self, df: pd.DataFrame) -> str`: Consolida las misiones y devuelve el resultado como una cadena.
- `calculate_percentages(self, df: pd.DataFrame) -> str`: Calcula los porcentajes y devuelve el resultado como una cadena.
- `move_devices_to_backup(self) -> None`: Mueve todas las subcarpetas de la carpeta 'devices' a la carpeta 'backups'.
- `run_reporte(reporte_path: str) -> None`: Método estático para ejecutar la generación de informes.

## Ejecución del Reporte

Para ejecutar el módulo de Reporte, puedes usar el siguiente código en tu archivo Apolo_11.py:

```python
from Reporte import ReportGenerator


# Rutas de los archivos generados y donde se guardarán los informes
devices_folder = "devices"
reports_folder = "reports"

# Ejecuta el generador de informes
ReportGenerator(devices_folder, reports_folder).run_reporte()

```

# Apolo_11.py

Este script sirve como punto de entrada para ejecutar Proyecto.py o Reporte.py en el contexto de Apolo_11.

## Ejecución:

```bash
python Apolo_11.py proyecto  # Para ejecutar el proyecto
python Apolo_11.py reporte   # Para ejecutar el reporte

```



