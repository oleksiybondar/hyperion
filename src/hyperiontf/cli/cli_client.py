from .base_shell import BaseShell, DEFAULT_EXIT_CODE_COMMAND

from ptyprocess import PtyProcess
from hyperiontf.logging import getLogger
from hyperiontf.typing import (
    LoggerSource,
    CommandExecutionException,
)

from hyperiontf.configuration.config import config
import time


EXIT_CODES_COMMANDS = {
    "cmd": "echo %ERRORLEVEL%",
    "powershell": "echo $LASTEXITCODE",
}

logger = getLogger(LoggerSource.CLI)


class CLIClient(BaseShell):
    """
    A client class for interacting with command-line interfaces (CLI) through a persistent shell session.

    This class provides methods to execute both interactive and non-interactive commands, cache and retrieve output,
    verify exit codes, and perform assertions on command results. It is designed to work with different shell environments
    like bash, sh, zsh, cmd, and PowerShell.

    Key features include:
    - Persistent shell session using `PtyProcess`.
    - Command execution (both interactive and non-interactive).
    - Output caching and retrieval.
    - Exit code verification and assertion.
    - Log generation for all critical actions, including command execution and session management.

    Methods starting with `assert_*` raise exceptions on failure, while methods starting with `verify_*`
    return `True` or `False`, allowing non-blocking checks.

    :param shell: The shell to be used for the session (default: 'bash').
    """

    def __init__(self, shell="bash"):
        """
        Initializes the CLIClient for a specific shell.

        :param shell: The shell to be used (e.g., 'bash', 'sh', 'zsh', 'cmd', 'powershell').
        """
        super().__init__()

        self.source = shell
        self.process = None
        self.exit_code_cmd = self._fetch_exit_code_cmd()

        self.start_session()

    @property
    def shell(self) -> str:
        return self.source

    def start_session(self):
        """
        Starts a persistent shell session using PtyProcess.

        This method spawns a new session in the specified shell. If the session fails to start,
        an exception is logged and raised.

        :raises CommandExecutionException: If the shell session cannot be started.
        """
        try:
            # Start a new shell session using PtyProcess
            self.process = PtyProcess.spawn([self.shell])
            self._log_action(f"Spawning a new {self.shell} session.")
            time.sleep(
                config.cli.command_registration_time
            )  # make sure the shel loaded
            self._detect_action_prompt()

        except Exception as e:
            self._log_error(
                f"Failed to start shell session: {str(e)}", CommandExecutionException
            )

    def _read_output_buffer(self) -> str:
        """
        Reads and decodes the current buffer from the shell session.

        This method retrieves data from the shell process, decodes it from bytes to a string,
        and strips any leading/trailing whitespace.

        :return: The decoded output from the shell.
        """
        data = self.process.read().decode().strip()
        self._log_debug(f"Reading output chunk:\n{data}")
        return data

    def _write(self, data: str):
        """
        Sends a command or input to the shell session.

        This method writes the provided command or input string to the shell's input stream,
        followed by a newline character.

        :param data: The string to write to the shell session.
        """
        self._log_debug(f"Writing data chunk:\n{data}")
        self.process.write(f"{data}\n".encode("utf-8"))
        time.sleep(config.cli.command_registration_time)

    def _fetch_exit_code_cmd(self):
        """
        Retrieves the appropriate command to fetch the exit code for the current shell.

        This method returns the shell-specific command for retrieving the exit code of the last executed command.

        :return: The shell command to fetch the exit code.
        """
        return EXIT_CODES_COMMANDS.get(self.shell, DEFAULT_EXIT_CODE_COMMAND)

    def quit(self):
        """
        Terminates the shell session.
        """
        if self.process:
            self._log_action("Terminating session.")
            self.process.terminate()
