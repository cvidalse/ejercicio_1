from conf.Configuration_manager import Configuration_manager
import importlib

config = Configuration_manager.load_config()

# Modelo cargado desde un archivo de configuración
Controller = getattr(importlib.import_module(
    "controllers." + config['run_controller']),  config['run_controller'])

controller = Controller()

controller.run()
