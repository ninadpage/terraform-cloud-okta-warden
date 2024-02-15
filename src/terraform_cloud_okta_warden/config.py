"""Config for the CLI."""
from pydantic import AnyUrl
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TerraformCloudConfig(BaseSettings):
    """noqa: D101."""

    url: AnyUrl
    organization_name: str
    token: SecretStr


class OktaConfig(BaseSettings):
    """noqa: D101."""

    org_url: AnyUrl
    token: SecretStr


class AppConfig(BaseSettings):
    """noqa: D101."""

    okta: OktaConfig
    tfc: TerraformCloudConfig
