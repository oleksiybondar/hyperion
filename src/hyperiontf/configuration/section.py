class Section:
    """
    Base class for config sections.
    """

    def _iter_attributes(self):
        """
        Iterate over attributes that are not callable and don't start with an underscore.
        """
        for key in dir(self):
            if key.startswith("_") or callable(getattr(self, key)):
                continue
            yield key

    def from_cfg_node(self, cfg_node: dict):
        """
        Update class attributes with values from a configuration node.

        Parameters:
            cfg_node (dict): Dictionary containing configuration values.

        This method iterates over the class attributes, excluding callable attributes and
        those starting with an underscore (_), and updates them with the values from the
        provided configuration node if they exist.
        """
        for key in self._iter_attributes():
            value = cfg_node.get(key)
            if value is not None:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        """
        Convert the config section attributes to a dictionary.

        Returns:
            dict: A dictionary containing the config section attributes.
        """
        return {key: getattr(self, key) for key in self._iter_attributes()}
