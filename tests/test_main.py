"""Test cases for the __main__ module."""
import logging

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from terraform_cloud_okta_warden.__main__ import app


CLI_ARGS = ["--okta-org-url=https://example.okta.com", "--tfc-org-name=example"]


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def env_vars(monkeypatch: MonkeyPatch) -> None:
    """Mocks required environment variables."""
    monkeypatch.setenv("OKTA_TOKEN", "okta-token")
    monkeypatch.setenv("TFC_TOKEN", "tfc-token")


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0


def test_coloredlogs_config_tty(
    runner: CliRunner, env_vars: None, monkeypatch: MonkeyPatch, mocker: MockerFixture
) -> None:
    """Test tty is only set for CI environment."""
    mocked_install = mocker.patch("terraform_cloud_okta_warden.__main__.coloredlogs.install")

    monkeypatch.delenv("CI", raising=False)
    result = runner.invoke(app, ["--log-level=INFO", *CLI_ARGS])
    assert result.exit_code == 0
    mocked_install.assert_called_once_with(level=logging.INFO)

    mocked_install.reset_mock()
    monkeypatch.setenv("CI", "true")
    runner.invoke(app, ["--log-level=INFO", *CLI_ARGS])
    mocked_install.assert_called_once_with(level=logging.INFO, isatty=True)


def test_coloredlogs_log_level_warn(runner: CliRunner, env_vars: None) -> None:
    """Test special handling for DEBUG logging."""
    runner.invoke(app, ["--log-level=WARN", *CLI_ARGS])
    assert logging.getLogger().getEffectiveLevel() == logging.WARN
    assert (
        logging.getLogger("terraform_cloud_okta_warden.__main__").getEffectiveLevel()
        == logging.WARN
    )

    # Debug logging should be set only for the main logger, with root logger at INFO
    runner.invoke(app, ["--log-level=DEBUG", *CLI_ARGS])
    assert logging.getLogger().getEffectiveLevel() == logging.INFO
    assert (
        logging.getLogger("terraform_cloud_okta_warden.__main__").getEffectiveLevel()
        == logging.DEBUG
    )
