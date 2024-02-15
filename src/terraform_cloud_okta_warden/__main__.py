"""Command-line interface."""
import logging
import os
from typing import Optional

import coloredlogs
import typer

from terraform_cloud_okta_warden import __version__
from terraform_cloud_okta_warden.config import AppConfig
from terraform_cloud_okta_warden.config import OktaConfig
from terraform_cloud_okta_warden.config import TerraformCloudConfig
from terraform_cloud_okta_warden.okta import OktaUserStatus
from terraform_cloud_okta_warden.okta import list_okta_users
from terraform_cloud_okta_warden.terraform_cloud import list_tfc_user_emails


logger = logging.getLogger("terraform_cloud_okta_warden")
app = typer.Typer()


def version_callback(value: Optional[bool]) -> None:
    """Prints current version and exits."""
    if value:
        typer.echo(f"terraform-cloud-okta-warden: {__version__}")
        raise typer.Exit()


def warn_about_nonactive_users(
    tfc_user_emails: list[str], okta_users: dict[str, OktaUserStatus]
) -> int:
    """Warns about non-users Terraform Cloud Organization."""
    count = 0
    for email in tfc_user_emails:
        if email not in okta_users:
            logger.warning(
                f"User {email!r} is a member of the TFC organization, but not present in Okta."
            )
            count += 1
            continue
        if okta_users[email] != OktaUserStatus.ACTIVE:
            logger.warning(
                f"User {email!r} is a member of the TFC organization, but their status "
                f"in Okta is {okta_users[email].value!r}."
            )
            count += 1
    logger.info(f"Affected users found: {count}")
    return count


@app.command()
def cli(
    okta_org_url: str = typer.Option(  # noqa: B008
        ..., help="Your Okta domain url (e.g. https://mycompany.okta.com)"
    ),
    okta_token: str = typer.Argument(  # noqa: B008
        ..., envvar="OKTA_TOKEN", help="Okta API token with access to list users"
    ),
    tfc_org_name: str = typer.Option(..., help="Terraform Cloud Organization name"),  # noqa: B008
    tfc_token: str = typer.Argument(  # noqa: B008
        ..., envvar="TFC_TOKEN", help="Terraform Cloud token with access to list users"
    ),
    tfc_url: str = typer.Option(  # noqa: B008
        "https://app.terraform.io",
        help="Defaults to Terraform Cloud, provide the URL if you use Terraform Enterprise",
    ),
    version: Optional[bool] = typer.Option(  # noqa: B008, F841
        None, "--version", callback=version_callback, is_eager=True
    ),
    log_level: str = "INFO",
) -> None:
    """Checks for existence of non-active Okta users in Terraform Cloud organization.

    Non-active users are those who are missing or de-provisioned in Okta.
    """
    coloredlogs_args = {}
    if os.getenv("CI"):
        # force tty for colors when running in CI
        coloredlogs_args["isatty"] = True
    level = coloredlogs.level_to_number(log_level.upper())
    if level > logging.DEBUG:
        coloredlogs.install(level=level, **coloredlogs_args)
    else:
        # Only set DEBUG level for the CLI logger and keep other loggers at INFO
        coloredlogs.install(level="INFO", **coloredlogs_args)
        logger.propagate = False
        coloredlogs.install(logger=logger, level=level, **coloredlogs_args)

    config = AppConfig(
        okta=OktaConfig(org_url=okta_org_url, token=okta_token),
        tfc=TerraformCloudConfig(url=tfc_url, organization_name=tfc_org_name, token=tfc_token),
    )
    tfc_user_emails = list_tfc_user_emails(config.tfc)
    okta_users = list_okta_users(config.okta)
    warn_about_nonactive_users(tfc_user_emails, okta_users)


def main() -> None:  # pragma: no cover
    """Main entrypoint."""
    app()


if __name__ == "__main__":  # pragma: no cover
    app()
