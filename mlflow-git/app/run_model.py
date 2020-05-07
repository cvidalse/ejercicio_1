from build_models.TensorFlowRun import TensorFlowRun
from conf.Configuration_manager import Configuration_manager
import importlib

config = Configuration_manager.load_config()

# Modelo cargado desde un archivo de configuración
BuildModel = getattr(importlib.import_module(
    "build_models." + config['build_model']),  config['build_model'])

model = BuildModel()

model.run()

