from hyperiontf.helpers.decorators.singleton import Singleton
from hyperiontf.helpers.string_helpers import camel_to_snake_case
from hyperiontf.configuration.sections import (
    Logger,
    Element,
    PageObject,
    DesktopCapabilities,
    WebCapabilities,
    Visual,
)
from hyperiontf.configuration.sections import Rest, MobileCapabilities

import os


@Singleton
class Config:
    """
    Represents the entire configuration.

    This class holds instances of individual section classes and provides methods to
    load the configuration from different file formats (JSON, YAML) and initialize
    the config sections accordingly.
    """

    def __init__(self):
        self.logger = Logger()
        self.page_object = PageObject()
        self.element = Element()
        self.web_capabilities = WebCapabilities()
        self.mobile_capabilities = MobileCapabilities()
        self.desktop_capabilities = DesktopCapabilities()
        self.rest = Rest()
        self.visual = Visual()

    def _parse_config_data(self, data):
        """
        Parse configuration data and update the sections.

        Parameters:
            data (dict): Dictionary containing the configuration data.

        This method iterates over the data and updates the corresponding sections
        in the configuration based on the section names and their data.
        """
        for section_name, section_data in data.items():
            section_name = camel_to_snake_case(section_name)
            _section_instance = getattr(self, section_name, None)
            if _section_instance:
                _section_instance.from_cfg_node(section_data)

    def update_from_cfg_file(self, cfg_file):
        """
        Update the configuration from a cfg, JSON, or YAML file.

        Parameters:
            cfg_file (str): Path to the cfg, JSON, or YAML file.

        This method reads the file, parses its contents, and updates the
        configuration sections accordingly.
        """
        _, file_extension = os.path.splitext(cfg_file)

        if file_extension == ".cfg":
            self._update_from_cfg_file(cfg_file)
        elif file_extension == ".json":
            self._update_from_json_file(cfg_file)
        elif file_extension == ".yml" or file_extension == ".yaml":
            self._update_from_yml_file(cfg_file)

    def _update_from_cfg_file(self, cfg_file):
        import configparser

        # Use configparser to read cfg file
        config_parser = configparser.ConfigParser()
        config_parser.read(cfg_file)

        for section in config_parser.sections():
            for key, value in config_parser[section].items():
                # Update the section instance with key-value pair
                section_instance = getattr(self, camel_to_snake_case(section), None)
                if section_instance:
                    section_instance.from_cfg_node({key: value})

    def _update_from_json_file(self, cfg_file):
        with open(cfg_file, "r") as json_file:
            import json

            # Load JSON data from the file
            data = json.load(json_file)
            # Parse the data and update the sections
            self._parse_config_data(data)

    def _update_from_yml_file(self, cfg_file):
        import yaml

        with open(cfg_file, "r") as yaml_file:
            # Load YAML data from the file
            data = yaml.safe_load(yaml_file)
            # Parse the data and update the sections
            self._parse_config_data(data)


config = Config()
