from .base_shell import BaseShell
import paramiko
import shlex
from hyperiontf.typing import CommandExecutionException
from hyperiontf.configuration.config import config
import time
from hyperiontf.cli.helperes.ansi_escape import remove_ansi_sequences


class SSHClient(BaseShell):
    """
    A client class for interacting with remote machines over SSH through a persistent interactive SSH session.

    This class provides methods to execute both interactive and non-interactive commands, cache and retrieve output,
    and handle interactive SSH shells.

    It supports:
    - Persistent SSH session using `paramiko.SSHClient`.
    - Interactive input/output (send keys, receive output).
    - Exit code retrieval (for non-interactive commands).
    - Log generation for all critical actions, including command execution and session management.

    :param host: The remote host to connect to.
    :param user: The username for SSH authentication.
    :param password: The password for SSH authentication (optional if using key-based auth).
    :param private_key: The path to the private key for key-based authentication (optional if using password auth).
    :param port: The SSH port (default: 22).
    """

    def __init__(
        self,
        host,
        user,
        password=None,
        private_key=None,
        port=22,
        shell="bash",
        shell_args=None,
        env=None,
        disable_prompt_shortening: bool = True,
        cmd_line_matcher=None,
    ):
        super().__init__(
            shell=shell,
            shell_args=shell_args,
            env=env,
            disable_prompt_shortening=disable_prompt_shortening,
            cmd_line_matcher=cmd_line_matcher,
        )

        self.host = host
        self.user = user
        self.password = password
        self.private_key = private_key
        self.port = port
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.shell = None

        self.start_session()

    @property
    def line_separator(self) -> str:
        return "\r\n"

    def start_session(self):
        """
        Establishes an interactive SSH session using Paramiko.

        This method attempts to authenticate either using a password or a private key and
        spawns a new interactive shell session.

        :raises CommandExecutionException: If the SSH connection cannot be established.
        """
        try:
            self._log_action(f"Connecting to {self.host} as {self.user}.")
            self._connect()
            self._log_action("SSH session established.")

            self.shell = self._invoke_shell_with_environment()
            time.sleep(
                config.cli.ssh_connection_explicit_wait
            )  # Wait for shell to initialize

            self._activate_requested_shell()

            self._detect_action_prompt()

            self._prepare_prompt_settings()

        except Exception as e:
            self._log_error(
                f"Failed to establish SSH connection: {str(e)}",
                CommandExecutionException,
            )

    def _connect(self):
        if self.private_key:
            self._connect_using_private_key()
            return
        self._connect_using_password()

    def _invoke_shell_with_environment(self):
        if not self.env:
            return self.ssh_client.invoke_shell()
        try:
            return self.ssh_client.invoke_shell(environment=self.env)
        except TypeError:
            return self.ssh_client.invoke_shell()

    def _prepare_prompt_settings(self):
        if self.disable_prompt_shortening and self._is_posix_shell_prompt():
            self._apply_remote_prompt_settings()
            self.action_prompt = "hyperion$"

    def _activate_requested_shell(self):
        if not self.shell:
            return
        shell_executable = self._shell_executable or "bash"
        shell_argv = [shell_executable, *self.shell_args]
        shell_command = "exec " + shlex.join(shell_argv)
        self.shell.send(f"{shell_command}\n")
        time.sleep(config.cli.command_registration_time)

    def _connect_using_private_key(self):
        self.ssh_client.connect(
            hostname=self.host,
            username=self.user,
            key_filename=self.private_key,
            port=self.port,
        )

    def _connect_using_password(self):
        self.ssh_client.connect(
            hostname=self.host,
            username=self.user,
            password=self.password,
            port=self.port,
        )

    def _write(self, data: str):
        """
        Sends input to the SSH shell (for interactive commands).

        :param data: The string to send as input to the SSH shell.
        """
        if self.shell:
            self._log_debug(f"Sending input: {data}")
            self.shell.send(f"{data}\n")
            time.sleep(
                config.cli.command_registration_time
            )  # Allow time for the command to execute

    def _read_output_buffer(self) -> str:
        """
        Reads available output from the interactive SSH shell.

        This method reads the output from the SSH shell dynamically,
        allowing you to capture the result of an interactive command.

        :return: The output from the SSH shell as a string.
        """
        if self.shell:
            # if self.shell.recv_ready():
            output = self.shell.recv(1536).decode("utf-8")  # Read 1024 bytes at a time
            output = remove_ansi_sequences(output)
            self._log_debug(f"Reading shell output chunk: {output.strip()}")
            return output.strip()
        return ""

    def quit(self):
        """
        Terminates the SSH session.
        """
        if self.shell:
            self._log_action("Closing SSH interactive shell.")
            self.shell.close()
        if self.ssh_client:
            self._log_action("Terminating SSH session.")
            self.ssh_client.close()

    def _apply_remote_prompt_settings(self):
        if not self.shell:
            return
        self.shell.send("export PS1='hyperion$'\n")
        self.shell.send("export PROMPT='hyperion$'\n")
        self.shell.send("export COLUMNS=1024\n")
        self.shell.send("\n")
        time.sleep(config.cli.command_registration_time)
        try:
            # Drain one noisy chunk produced by prompt reconfiguration.
            self._read_output_buffer()
        except Exception:
            pass
