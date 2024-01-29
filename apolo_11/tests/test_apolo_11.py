import os
import sys
from io import StringIO
from unittest.mock import patch, Mock

# Agrega el directorio principal del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "apolo_11")))

from Apolo_11 import main

def test_main_proyecto(monkeypatch):
    """
    Prueba la función main cuando se selecciona 'proyecto'.
    """
    with patch("argparse.ArgumentParser.parse_args", return_value=Mock(script="proyecto")) as mock_parse_args, \
         patch("builtins.open", side_effect=[StringIO('{"config_key": "config_value"}'), StringIO("some_data")]) as mock_open, \
         patch("os.path.exists", return_value=True) as mock_exists, \
         patch("Apolo_11.ConfigLoader") as mock_config_loader, \
         patch("Apolo_11.DataGenerator", autospec=True) as mock_data_generator, \
         patch("Apolo_11.DataGenerator.run_proyecto") as mock_run_proyecto:

        monkeypatch.setattr(os.path, "join", lambda x, y: f"{x}/{y}")  # Simula la función os.path.join
        main()

    # Verifica que las funciones se llamaron con los argumentos correctos
    mock_parse_args.assert_called_once_with()
    mock_config_loader.assert_called_once_with('{"config_key": "config_value"}')
    mock_data_generator.assert_called_once_with(mock_config_loader.return_value)
    mock_run_proyecto.assert_called_once_with('{"config_key": "config_value"}', 'path/to/Proyecto.py')
