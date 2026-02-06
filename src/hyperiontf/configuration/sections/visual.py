import os

from ..section import Section
from hyperiontf.typing import VisualMode, VisualModeType


class Visual(Section):
    """
    Represents the [visual] section in the config.
    """

    def __init__(self):
        """
        Represents the [visual] section in the config.

        `mode` behavior:
        - If `HYPERION_VISUAL_MODE` is set to "collect" (case-insensitive), defaults to COLLECT.
        - Otherwise defaults to COMPARE.
        - When assigned from config/env/runtime, accepts either a VisualMode or a string.
        """
        self.mode: VisualModeType = self._fetch_default_mode()
        self.default_mismatch_threshold: float = 5.0
        self.default_partial_mismatch_threshold: float = 0.5

    @staticmethod
    def _fetch_default_mode():
        value = os.environ.get("HYPERION_VISUAL_MODE", None)
        if value == VisualMode.COLLECT:
            return VisualMode.COLLECT

        return VisualMode.COMPARE
