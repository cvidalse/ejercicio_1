#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import os
from pathlib import Path

class Configuration_manager(object):
	"""Configuration loader
	
	This script loads the configuration from a file 'config.json'.
	
	"""

	@staticmethod
	def load_config():
		file_dir = os.path.dirname(os.path.abspath(__file__))
		file_route = '/config.json'
		file_option = 'r'
		with open(file_dir + file_route, file_option) as f:
			config = json.load(f)

		return config

	@staticmethod
	def save_values(config_data):

		file_dir = os.path.dirname(os.path.abspath(__file__))
		file_route = '/config.json'
		file_option = 'r+'

		with open(file_dir + file_route, file_option) as f:
			f.seek(0)        # <--- should reset file position to the beginning.
			json.dump(config_data, f, indent=4)
			f.truncate()  
