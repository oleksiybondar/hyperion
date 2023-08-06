from ..section import Section


class PageObject(Section):
    """
    Represents the [page_object] section in the config.
    """

    def __init__(self):
        self.start_retries = 3
        self.retry_delay = 1

        self.log_private = True

        self.viewport_xs = 0
        self.viewport_sm = 576
        self.viewport_md = 768
        self.viewport_lg = 992
        self.viewport_xl = 1200
        self.viewport_xxl = 1400
