class Section:
    """
    Base class for config sections.
    """

    def from_cfg_node(self, cfg_node: dict):
        """
        Update class attributes with values from a configuration node.

        Parameters:
            cfg_node (dict): Dictionary containing configuration values.

        This method iterates over the class attributes, excluding callable attributes and
        those starting with an underscore (_), and updates them with the values from the
        provided configuration node if they exist.
        """
        for key in dir(self):
            if key.startswith("_"):
                continue

            attr = getattr(self, key)
            if not callable(attr):
                value = cfg_node.get(key)
                if value is not None:
                    setattr(self, key, value)

    def to_dict(self) -> dict:
        """
        Convert the config section attributes to a dictionary.

        Returns:
            dict: A dictionary containing the config section attributes.
        """
        section_dict = {}
        for key in dir(self):
            if key.startswith("_"):
                continue

            attr = getattr(self, key)
            if not callable(attr):
                section_dict[key] = attr

        return section_dict
