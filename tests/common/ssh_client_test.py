import pytest
from hyperiontf import SSHClient, expect
from hyperiontf.executors.pytest import automatic_log_setup  # noqa: F401
from hyperiontf.executors.pytest import fixture
from hyperiontf.typing import CommandExecutionTimeoutException

TEST_USER = "ssh_test_user"
TEST_PASSWORD = "test_password"


@fixture(autouse=True, log=False)
def ssh_client(request):
    """
    Fixture to handle OPC UA connection setup and teardown.

    Connects to the OPC server before each test and disconnects after the test.
    """
    client = SSHClient("127.0.0.1", TEST_USER, TEST_PASSWORD)
    request.addfinalizer(client.quit)

    yield client


@pytest.mark.SSH
@pytest.mark.ExecuteCommand
def test_non_interactive_command_execution(ssh_client):
    """
    Test execution of a non-interactive command.

    This test runs a simple command like `whoami`, which does not require user interaction,
    and asserts that the output matches the expected value (the current test user).
    """
    ssh_client.execute("whoami")
    ssh_client.assert_output(TEST_USER)


@pytest.mark.SSH
@pytest.mark.ExecuteInteractiveCommand
def test_interactive_command_execution(ssh_client):
    """
    Test execution of an interactive command.

    This test runs an interactive command (e.g., 'read') that prompts the user for input,
    waits for the prompt, sends the input, and asserts that the output contains the input.
    """
    ssh_client.exec_interactive('read -p "Enter something:"')
    ssh_client.wait("Enter something:")
    ssh_client.send_keys("Hyperion")
    ssh_client.wait()
    ssh_client.assert_output("Enter something:\nHyperion")


@pytest.mark.SSH
@pytest.mark.ExitCode
@pytest.mark.expect
@pytest.mark.ExecuteCommand
def test_exit_code_assertion(ssh_client):
    """
    Test exit code assertion for a failed command.

    This test runs a command that is expected to fail (e.g., accessing a non-existent directory),
    and asserts that the exit code is non-zero (typically 1).
    """
    ssh_client.execute("ls /nonexistentdirectory")
    expect(ssh_client.exit_code).not_to_be(0)


@pytest.mark.SSH
@pytest.mark.ExecuteCommand
@pytest.mark.Timeout
def test_command_execution_with_timeout(ssh_client):
    """
    Test command execution with a timeout.

    This test runs a long-running command (e.g., 'sleep') and asserts that a timeout exception
    is raised if the command takes longer than the specified time limit.
    """
    with pytest.raises(CommandExecutionTimeoutException):
        ssh_client.execute("sleep 3", timeout=2)
