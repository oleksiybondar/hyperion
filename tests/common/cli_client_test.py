import pytest
from hyperiontf import CLIClient, expect
from hyperiontf.executors.pytest import hyperion_test_case_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture
import os
from hyperiontf.typing import CommandExecutionTimeoutException


@fixture(autouse=True, log=False)
def cli_client(request):
    """
    Fixture to handle OPC UA connection setup and teardown.

    Connects to the OPC server before each test and disconnects after the test.
    """
    client = CLIClient()
    request.addfinalizer(client.quit)

    yield client


@pytest.mark.CLI
@pytest.mark.ExecuteCommand
def test_non_interactive_command_execution(cli_client):
    """
    Test execution of a non-interactive command.

    This test runs a simple command like `pwd`, which does not require user interaction,
    and asserts that the output matches the expected value (the current working directory).
    """
    cli_client.execute("pwd")
    cli_client.assert_output(os.getcwd())


@pytest.mark.CLI
@pytest.mark.ExecuteInteractiveCommand
def test_interactive_command_execution(cli_client):
    """
    Test execution of an interactive command.

    This test runs an interactive command (e.g., 'read') that prompts the user for input,
    waits for the prompt, sends the input, and asserts that the output contains the input.
    """
    cli_client.exec_interactive('read -p "Enter something:"')
    cli_client.wait("Enter something:")
    cli_client.send_keys("Hyperion")
    cli_client.wait()
    cli_client.assert_output("Enter something:\nHyperion")


@pytest.mark.CLI
@pytest.mark.ExitCode
@pytest.mark.expect
@pytest.mark.ExecuteCommand
def test_exit_code_assertion(cli_client):
    """
    Test exit code assertion for a failed command.

    This test runs a command that is expected to fail (e.g., accessing a non-existent directory),
    and asserts that the exit code is non-zero (typically 1).
    """
    cli_client.execute("ls /nonexistentdirectory")
    expect(cli_client.exit_code).not_to_be(0)


@pytest.mark.CLI
@pytest.mark.ExecuteCommand
@pytest.mark.Timeout
def test_command_execution_with_timeout(cli_client):
    """
    Test command execution with a timeout.

    This test runs a long-running command (e.g., 'sleep') and asserts that a timeout exception
    is raised if the command takes longer than the specified time limit.
    """
    with pytest.raises(CommandExecutionTimeoutException):
        cli_client.execute("sleep 3", timeout=2)
