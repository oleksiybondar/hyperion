import os
import re
from typing import Optional, Union

from ptyprocess import PtyProcess
from hyperiontf.logging import getLogger
from hyperiontf.typing import (
    LoggerSource,
    CommandExecutionException,
    CommandExecutionTimeoutException,
)
from hyperiontf.configuration.config import config
from hyperiontf.assertions.expect import Expect
import time
import signal

DEFAULT_EXIT_CODE_COMMAND = "echo $?"

EXIT_CODES_COMMANDS = {
    "cmd": "echo %ERRORLEVEL%",
    "powershell": "echo $LASTEXITCODE",
}

logger = getLogger(LoggerSource.CLI)


class CLIClient:
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
        self.process = None
        self.output_cache = []
        self.exit_code = None
        self.shell = shell
        self.action_prompt = None
        self.last_cmd = None
        self.exit_code_cmd = self._fetch_exit_code_cmd()

        self.start_session()

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

    @property
    def output(self) -> str:
        """
        Returns the current output cache as a single string.

        :return: Cached output from the shell session, stripped of leading/trailing whitespace.
        """
        return "\n".join(self.output_cache).strip()

    def _cache_output(self):
        """
        Caches the current output from the shell session.

        This method reads the current buffer from the shell process, removes any prompt or
        command echoes, and appends the remaining output to the internal cache.
        """
        data = self._read_output_buffer()

        if not data:
            return

        if data == self.action_prompt:
            return

        lines = data.split(os.linesep)
        for line in lines:
            line = line.strip()

            if self._is_cmd_line(line):
                self.last_cmd = None
                continue

            self.output_cache.append(line)

    def _is_cmd_line(self, line: str) -> bool:
        # Pattern to match different shell prompt and command formats
        # - Full command only
        # - Prompt + command
        # - Shortened prompt due to path length
        # Example pattern: <path/end$ <cmd>

        # Define a regex pattern to match prompt variations
        pattern = r"^\s*<.*?(\$|\#)\s*"  # Matches <path$ or <path#

        if not self.last_cmd:
            return False
        # Check if the line matches the last command or one of the patterns
        return line == self.last_cmd or (
            self.last_cmd in line
            and (bool(re.search(pattern, line)) or self.action_prompt in line)
        )

    def _clear_cache(self):
        """
        Clears the internal output cache.

        This method is used to reset the cached output between commands.
        """
        self.output_cache = []

    def flush_output(self):
        """
        Clears the current output cache and resets it.

        This method also logs a message indicating the flush action.
        """
        self._log_debug("Flushing current output")
        self._clear_cache()

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

    def _detect_action_prompt(self):
        """
        Detects the shell's action prompt and stores it internally.

        This method reads the shell's output buffer to identify and store the action prompt,
        which is the marker used to indicate when a command has finished executing.
        """
        data = self._read_output_buffer()
        self.action_prompt = data.split("\n")[-1].strip()
        self._log_debug(f"Action prompt is:\n{self.action_prompt}")

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

    def _register_new_command(self, command: str):
        """
        Registers a new command execution by clearing the output cache and resetting state.

        This method prepares the client for executing a new command by clearing the cached output,
        resetting the exit code, and marking the new command as the `last_cmd`.

        :param command: The command that is being registered for execution.
        """
        self.flush_output()
        self.exit_code = None
        self.last_cmd = command

    def execute(
        self, command: str, timeout: Optional[int] = config.cli.execution_timeout
    ):
        """
        Executes a command in the shell session.

        This method sends the specified command to the shell session and waits for the
        shell prompt to return, indicating that the command has completed execution.

        :param command: The command to execute in the shell.
        :param timeout: Optional timeout for command execution. Defaults to the configured timeout.
        :raises CommandExecutionTimeoutException: If the command execution exceeds the timeout.
        """
        self._register_new_command(command)
        self._log_action(
            f"Executing command:\n{command}\nExecution limit: {timeout} seconds"
        )
        self._write(command)
        self._wait(
            self.action_prompt, timeout, "Waiting for next command prompt to appear."
        )

    def exec_interactive(self, command):
        """
        Executes an interactive command in the shell session.

        This method sends a command that requires user input (e.g., 'read'), allowing
        for further interaction through `send_keys`.

        :param command: The interactive command to execute.
        """
        self._register_new_command(command)
        self._log_action(
            f"Executing command:\n{command}\nExecution limit: no limit - Interactive mode."
        )
        self._write(command)

    def send_keys(self, data: str):
        """
        Sends keystrokes to the shell session, simulating user input.

        :param data: The string input to send to the interactive shell.
        """
        self._log_action(f"Sending interactive input:\n{data}")
        self._write(data)

    def wait(
        self,
        pattern: Optional[Union[str]] = None,
        timeout: int = config.cli.execution_timeout,
    ):
        """
        Waits for a specific pattern or the action prompt in the output.

        This method blocks execution until the specified pattern is found in the output or the timeout occurs.

        :param pattern: The output pattern to wait for. Defaults to the shell's action prompt.
        :param timeout: The maximum time to wait for the pattern. Defaults to the configured timeout.
        :raises CommandExecutionTimeoutException: If the pattern is not found within the timeout period.
        """
        if pattern is None:
            pattern = self.action_prompt
        self._wait(pattern, timeout, f"Waiting for following output: {pattern}")

    def _wait(self, pattern, timeout, message):
        """
        Waits for a specific pattern to appear in the shell output.

        This method blocks execution until the specified pattern is found in the output,
        or until the timeout is reached.

        :param pattern: The string pattern to search for in the output.
        :param timeout: The maximum time to wait for the pattern.
        :param message: A descriptive message logged during the wait process.
        :raises CommandExecutionTimeoutException: If the pattern is not found within the timeout.
        """
        logger.push_folder(message)
        found = False
        self._prepare_alarm(timeout)
        try:
            found = self._wait_loop(pattern)  # Simulate work in the main thread
        except TimeoutError:
            pass
        finally:
            self._reset_alarm()

        logger.pop_folder()

        if not found:
            self._log_error(
                f"{pattern} did not appeared in output withing {timeout} seconds",
                CommandExecutionTimeoutException,
            )

        self._fix_output_after_wait(pattern)

    def _prepare_alarm(self, timeout):
        """
        Sets up a system alarm to interrupt the process after a timeout.

        This method uses a signal-based alarm to trigger a `TimeoutError` if the
        specified timeout period is reached.

        :param timeout: The time in seconds after which the alarm will trigger.
        """
        signal.signal(signal.SIGALRM, self.alarm_handler)
        signal.alarm(timeout)

    @staticmethod
    def _reset_alarm():
        """
        Resets any active system alarms.

        This method cancels any pending alarms, ensuring no timeout interrupts occur.
        """
        signal.alarm(0)

    def _wait_loop(self, pattern):
        """
        Loops until the specified pattern is found in the shell output.

        This method continuously checks the shell's output for the given pattern,
        appending new output to the cache and sleeping between iterations.

        :param pattern: The string pattern to search for in the output.
        :return: True if the pattern is found, False otherwise.
        """
        found = False
        while not found:
            self._cache_output()
            if self.output.endswith(pattern):
                found = True
            time.sleep(config.cli.wait_idle_time)
        return found

    def _fetch_exit_code_cmd(self):
        """
        Retrieves the appropriate command to fetch the exit code for the current shell.

        This method returns the shell-specific command for retrieving the exit code of the last executed command.

        :return: The shell command to fetch the exit code.
        """
        return EXIT_CODES_COMMANDS.get(self.shell, DEFAULT_EXIT_CODE_COMMAND)

    def _fix_output_after_wait(self, pattern):
        """
        Adjusts the output cache after waiting for a pattern.

        If the pattern corresponds to the action prompt, this method removes the prompt from the output cache
        and retrieves the exit code of the last executed command.

        :param pattern: The pattern that was waited for (typically the action prompt).
        """
        if pattern == self.action_prompt:
            self._remove_action_prompt_from_output()
            self._fetch_exit_code()

    def _fetch_exit_code(self):
        """
        Sends the command to fetch the exit code and parses the result.

        This method writes the shell-specific command to retrieve the exit code, then
        reads and parses the output to store the exit code.
        """
        self._write(self.exit_code_cmd)
        time.sleep(config.cli.command_registration_time)
        self._parse_exit_code_output()

    def _parse_exit_code_output(self):
        """
        Parses the shell's output to extract the exit code.

        This method processes the output buffer to remove the command and action prompt,
        and converts the remaining value into an integer representing the exit code.
        """
        output = self._read_output_buffer()
        output = output.replace(self.exit_code_cmd, "")
        output = output.replace(self.action_prompt, "")
        self.exit_code = int(output)

    def _remove_action_prompt_from_output(self):
        """
        Removes the action prompt from the cached output.

        This method ensures that the shell's action prompt is not included in the cached output,
        keeping the cache clean and relevant to the executed command.
        """
        self.output_cache.pop()

    def quit(self):
        """
        Terminates the shell session.
        """
        if self.process:
            self._log_action("Terminating session.")
            self.process.terminate()

    def assert_exit_code(self, expected_code: int):
        """
        Asserts that the last executed command's exit code matches the expected code.

        This method will raise an exception if the assertion fails.

        :param expected_code: The expected exit code from the last command.
        :raises FailedExpectationException: If the exit code does not match the expected code.
        """
        return self._prepare_expect_object(self.exit_code).to_be(expected_code)

    def verify_exit_code(self, expected_code: int):
        """
        Verifies that the last executed command's exit code matches the expected code.

        This method will log the verification result but will not raise an exception if it fails.

        :param expected_code: The expected exit code from the last command.
        :return: True if the exit code matches, False otherwise.
        """
        return self._prepare_verify_object(self.exit_code).to_be(expected_code)

    def assert_output(self, expected_output: str):
        """
        Asserts that the current output matches the expected output.

        :param expected_output: The output to compare with the shell's current output.
        :raises FailedExpectationException: If the output does not match the expected output.
        """
        return self._prepare_expect_object(self.output).to_be(expected_output)

    def verify_output(self, expected_output: str):
        """
        Verifies that the current output matches the expected output.

        :param expected_output: The output to compare with the shell's current output.
        :return: True if the output matches, False otherwise.
        """
        return self._prepare_verify_object(self.output).to_be(expected_output)

    def assert_output_contains(self, expected_output: str):
        """
        Asserts that the current output contains the specified substring.

        :param expected_output: The substring to search for in the shell's current output.
        :raises FailedExpectationException: If the substring is not found in the output.
        """
        return self._prepare_expect_object(self.output).to_contain(expected_output)

    def verify_output_contains(self, expected_output: str):
        """
        Verifies that the current output contains the specified substring.

        :param expected_output: The substring to search for in the shell's current output.
        :return: True if the substring is found, False otherwise.
        """
        return self._prepare_verify_object(self.output).to_contain(expected_output)

    def _log_debug(self, message: str):
        """
        Logs a debug message specific to the CLI client.

        :param message: The message to log at the debug level.
        """
        logger.debug(self._compose_log_message(message))

    def _log_action(self, message: str):
        """
        Logs an informational message describing a key action.

        :param message: The message to log at the info level.
        """
        logger.info(self._compose_log_message(message))

    def _log_error(self, message: str, exception_class):
        """
        Logs a critical error message and raises an exception.

        This method logs the error message at the critical level and raises the specified exception class.

        :param message: The error message to log.
        :param exception_class: The exception class to raise.
        """
        logger.critical(self._compose_log_message(message))
        raise exception_class(message)

    def _compose_log_message(self, message) -> str:
        """
        Composes a log message that includes the current shell context.

        This method prefixes the log message with the shell name to provide context for the log entry.

        :param message: The original message to log.
        :return: The log message prefixed with the shell name.
        """
        return f"[{self.shell}] {message}"

    def _prepare_expect_object(self, value, is_assertion: bool = True):
        return Expect(
            value,
            is_assertion=is_assertion,
            sender=self.shell,
            logger=logger,
        )

    def _prepare_verify_object(self, value):
        return self._prepare_expect_object(value, False)

    @staticmethod
    def alarm_handler(signum, frame):
        """
        Signal handler for the system alarm.

        This method is triggered when the system alarm goes off, raising a `TimeoutError` to interrupt execution.

        :param signum: The signal number (typically `SIGALRM`).
        :param frame: The current stack frame (unused).
        :raises TimeoutError: Indicates that the execution time has expired.
        """
        raise TimeoutError("Execution time expired!")
