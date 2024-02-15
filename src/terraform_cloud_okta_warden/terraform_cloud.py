"""Okta API utils."""
import logging

from terrasnek.api import TFC

from terraform_cloud_okta_warden.config import TerraformCloudConfig


logger = logging.getLogger(__name__)


def list_tfc_user_emails(tfc_config: TerraformCloudConfig) -> list[str]:  # pragma: no cover
    """List emails of users who are members of the given TFC org."""
    api = TFC(tfc_config.token.get_secret_value(), url=tfc_config.url.unicode_string())
    api.set_org(tfc_config.organization_name)

    user_emails = []
    try:
        resp = api.org_memberships.list_for_org()
        while True:
            user_emails.extend([user["attributes"]["email"] for user in resp["data"]])
            next_page = resp["meta"]["pagination"]["next-page"]
            if next_page:
                resp = api.org_memberships.list_for_org(page=next_page)
            else:
                break

        return user_emails
    except Exception as error:
        logger.exception(f"Error while fetching users from Terraform Cloud: {error}")
        raise
