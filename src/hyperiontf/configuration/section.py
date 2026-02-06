import os
from typing import Optional

ENV_OVERWRITE_MAP = {
    "log_folder": "HYPERION_LOG_FOLDER",
    "mode": "HYPERION_VISUAL_MODE",
}

ENV_TYPE_MAP = {
    "log_folder": "str",
    "mode": "str",
}


class Section:
    """
    Base class for configuration sections.

    Precedence rules (highest to lowest):

      1) Explicit runtime assignments (e.g. `config.logger.log_folder = "x"`)
      2) Environment variable overrides (e.g. `HYPERION_LOG_FOLDER`)
      3) Values from configuration files (ini/conf/cfg/json/yaml)
      4) Section defaults defined in `__init__`

    Notes:
    - Environment variable overrides are applied when configuration is loaded
      via `from_cfg_node()` (i.e. during config file parsing/updates).
    - This class only sets attributes that are already exposed by the section
      (via `_iter_attributes()`); unknown config keys are ignored.
    """

    def _iter_attributes(self):
        """
        Yield public, non-callable attribute names for this section.

        This iterator intentionally excludes:
        - private/internal names (starting with "_")
        - callables (methods/functions)

        It includes properties, which allows `setattr()` to trigger property setters
        (used to enforce invariants such as directory creation for log folders).

        Returns:
            Iterable[str]: Attribute names that represent configurable fields.
        """
        for key in dir(self):
            if key.startswith("_") or callable(getattr(self, key)):
                continue
            yield key

    def from_cfg_node(self, cfg_node: dict):
        """
        Apply configuration values from a single parsed configuration node.

        This method updates only attributes exposed by the section itself
        (see `_iter_attributes()`), and uses the following precedence:

        - If an environment variable override is defined for a field and present
          in the process environment, it is applied (after type conversion).
        - Otherwise, if the field exists in `cfg_node`, the config value is applied.
        - Otherwise, the current value (usually a default) remains unchanged.

        Parameters:
            cfg_node (dict): A dictionary of configuration values for this section.
                Typically produced by parsing JSON/YAML or INI/CFG/CONF sections.
        """
        for key in self._iter_attributes():
            env_value = self.fetch_env_overwrite_value(key)
            if env_value is not None:
                self._set_env_value(env_value, key)
            else:
                self._set_config_value(cfg_node, key)

    def _set_config_value(self, cfg_node, key):
        """
        Apply a value from the provided configuration node if present.

        Parameters:
            cfg_node (dict): Parsed configuration values for the section.
            key (str): Field name to apply.

        Notes:
            - If `key` is not present in `cfg_node` or maps to None, no update occurs.
            - If the target attribute is a property, its setter will be invoked.
        """
        value = cfg_node.get(key)
        if value is not None:
            setattr(self, key, value)

    def _set_env_value(self, env_value, key):
        """
        Apply a value from an environment variable override.

        Parameters:
            env_value (str): Raw environment variable value.
            key (str): Field name to apply.

        Notes:
            - The raw string is converted using `convert_env_value_to_type()`.
            - If conversion returns None, the update is skipped.
            - If the target attribute is a property, its setter will be invoked.
        """
        value = self.convert_env_value_to_type(env_value, key)
        if value is not None:
            setattr(self, key, value)

    @staticmethod
    def convert_env_value_to_type(env_value, key):
        """
        Convert a raw environment variable string into the configured field type.

        Parameters:
            env_value (str): Raw environment variable value.
            key (str): The field name being overridden.

        Returns:
            Any: The converted value. Currently defaults to string conversion.

        Notes:
            - Type conversion is controlled by `ENV_TYPE_MAP`.
            - At the moment, only `"str"` is implemented.
            - Extend this function to support additional types (bool, int, float, etc.)
              using deterministic parsing rules.
        """
        type_name = ENV_TYPE_MAP.get(key, "str")
        if type_name == "str":
            return env_value
        # TODO: add more types as needed
        return env_value

    @staticmethod
    def fetch_env_overwrite_value(key: str) -> Optional[str]:
        """
        Fetch an environment variable value for a section field, if configured.

        Parameters:
            key (str): Field name to check.

        Returns:
            Optional[str]: The environment variable value if:
              - the field is mapped in `ENV_OVERWRITE_MAP`, and
              - the environment variable is present in `os.environ`
            Otherwise returns None.
        """
        env_name = ENV_OVERWRITE_MAP.get(key, None)
        if not env_name:
            return None
        return os.environ.get(env_name, None)

    def to_dict(self) -> dict:
        """
        Convert this configuration section into a dictionary.

        Returns:
            dict: A mapping of each exposed field name (from `_iter_attributes()`)
            to its current value.
        """
        return {key: getattr(self, key) for key in self._iter_attributes()}
