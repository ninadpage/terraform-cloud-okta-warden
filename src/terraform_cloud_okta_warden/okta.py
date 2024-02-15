"""Okta API utils."""
import asyncio
import logging
from enum import Enum

from okta.client import Client as OktaClient
from okta.exceptions import OktaAPIException

from terraform_cloud_okta_warden.config import OktaConfig


logger = logging.getLogger(__name__)


class OktaUserStatus(Enum):
    """Okta user status values."""

    STAGED = "STAGED"
    PROVISIONED = "PROVISIONED"
    ACTIVE = "ACTIVE"
    RECOVERY = "RECOVERY"
    LOCKED_OUT = "LOCKED_OUT"
    PASSWORD_EXPIRED = "PASSWORD_EXPIRED"  # nosec B105
    SUSPENDED = "SUSPENDED"
    DEPROVISIONED = "DEPROVISIONED"


async def _list_okta_users(
    okta_config: OktaConfig, status: OktaUserStatus
) -> dict[str, OktaUserStatus]:  # pragma: no cover
    """Internal async function to list Okta users with the given status."""
    okta_client = OktaClient(
        {
            "orgUrl": okta_config.org_url.unicode_string(),
            "token": okta_config.token.get_secret_value(),
            "raiseException": True,
        }
    )

    okta_users = {}

    try:
        users, resp, err = await okta_client.list_users(
            query_params={"filter": f'status eq "{status.value}"'}  # noqa B907
        )
        while True:
            for user in users:
                okta_users[str(user.profile.email).lower()] = status
            if resp.has_next():
                users, err = await resp.next()
            else:
                break

        return okta_users
    except OktaAPIException as error:
        logger.exception(f"Error while fetching users from Okta: {error}")
        raise


def list_okta_users(okta_config: OktaConfig) -> dict[str, OktaUserStatus]:
    """Lists Okta users along with their activation status.

    Returns a dict with user emails as keys and their respective statuses as values.
    """
    loop = asyncio.get_event_loop()
    okta_users = {}
    for status in OktaUserStatus:
        okta_users.update(loop.run_until_complete(_list_okta_users(okta_config, status)))
    return okta_users
