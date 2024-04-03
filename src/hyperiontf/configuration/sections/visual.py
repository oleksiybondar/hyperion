from ..section import Section
from hyperiontf.typing import VisualMode, VisualModeType


class Visual(Section):
    """
    Represents the [visual] section in the config.
    """

    def __init__(self):
        self.mode: VisualModeType = VisualMode.COMPARE
        self.default_mismatch_threshold: float = 5.0
        self.default_partial_mismatch_threshold: float = 0.5
