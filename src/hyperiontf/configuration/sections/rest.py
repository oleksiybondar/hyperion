from ..section import Section


class Rest(Section):
    """
    Represents the [rest] section in the config.
    """

    def __init__(self):
        self.follow_redirects = True
        self.post_redirect_get = False
        self.accept_errors = False
        self.redirections_limit = 20
        self.connection_timeout = 10
        self.request_timeout = 30
        self.log_redirects = False
