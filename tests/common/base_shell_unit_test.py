import pytest

from hyperiontf.cli.base_shell import BaseShell
from hyperiontf.cli.cli_client import CLIClient


class DummyShell(BaseShell):
    def start_session(self):
        pass

    def _write(self, data: str):
        pass

    def _read_output_buffer(self) -> str:
        return ""


@pytest.mark.CLI
def test_compose_spawn_env_respects_external_env_overrides():
    shell = DummyShell(
        shell="bash",
        env={"HYPERION_TEST_ENV": "enabled"},
        disable_prompt_shortening=True,
    )
    env = shell._compose_spawn_env()

    assert env["HYPERION_TEST_ENV"] == "enabled"


@pytest.mark.CLI
def test_compose_spawn_argv_includes_shell_args():
    shell = DummyShell(shell="bash", shell_args=["--noprofile", "--norc"])
    assert shell._compose_spawn_argv() == ["bash", "--noprofile", "--norc"]


@pytest.mark.CLI
def test_cli_client_adds_default_shell_args_for_bash_when_prompt_shortening_disabled(
    monkeypatch,
):
    captured = {}

    class FakeProcess:
        @staticmethod
        def read():
            return b"hyperion$ "

        @staticmethod
        def write(_data):
            return None

        @staticmethod
        def terminate():
            return None

    def fake_spawn(
        argv,
        cwd=None,
        env=None,
        echo=True,
        preexec_fn=None,
        dimensions=(24, 80),
        pass_fds=(),
    ):
        captured["argv"] = argv
        captured["env"] = env
        return FakeProcess()

    monkeypatch.setattr("hyperiontf.cli.cli_client.PtyProcess.spawn", fake_spawn)

    client = CLIClient(
        shell="bash",
        env={"HYPERION_TEST_ENV": "enabled"},
        disable_prompt_shortening=True,
    )
    try:
        assert captured["argv"][:3] == ["bash", "--noprofile", "--norc"]
        assert captured["env"]["HYPERION_TEST_ENV"] == "enabled"
    finally:
        client.quit()
