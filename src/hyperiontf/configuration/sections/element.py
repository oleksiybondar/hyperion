from ..section import Section


class Element(Section):
    """
    Represents the [element] section in the config.
    """

    def __init__(self):
        self.search_attempts = 3
        self.search_retry_timeout = 0.5
        self.stale_recovery_timeout = 0.5
        self.wait_timeout = 30
        self.missing_timeout = 5
