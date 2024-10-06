from ..section import Section


class CLI(Section):
    """
    Represents the [rest] section in the config.
    """

    def __init__(self):
        self.execution_timeout = 60
        self.wait_idle_time = 1
        self.command_registration_time = 0.3
        self.ssh_connection_explicit_wait = 1
