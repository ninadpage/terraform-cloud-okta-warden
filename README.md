# Terraform Cloud Okta Warden

[![PyPI](https://img.shields.io/pypi/v/terraform-cloud-okta-warden.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/terraform-cloud-okta-warden.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/terraform-cloud-okta-warden)][pypi status]
[![License](https://img.shields.io/pypi/l/terraform-cloud-okta-warden)][license]

[![Tests](https://github.com/ninadpage/terraform-cloud-okta-warden/workflows/Tests/badge.svg)][tests]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/terraform-cloud-okta-warden/
[tests]: https://github.com/ninadpage/terraform-cloud-okta-warden/actions?workflow=Tests
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## What is this?

If you use Terraform Cloud and have configured SSO for it via Okta (or any other IdP), it's critical
to be aware of the fact that login via SSO is not always enforced by Terraform Cloud.

In certain scenarios (as tested in February 2024), one can still access your Terraform Cloud
organization even if their account in the IdP is de-provisioned:

- If you have not taken steps to ensure when a user is de-provisioned your IdP, their TFC account is
  also removed from your Terraform Cloud organization. This does not happen automatically as TFC
  does not support SCIM, so it has to be a manual process as part of users' off-boarding flow, or
  you must implement a custom solution using your IdP's API/Workflows and TFC API.
- If the user had set the password (with optional TOTP as 2FA) to their TFC account and they might
  still have the credentials stored.

  Then they can login to Terraform Cloud, but cannot access your Organization via UI (they
  will be prompted to re-login with SSO). However, **they can create an API token** and regain the
  same level of access they had before their account was de-provisioned. Any API tokens they had
  created before would also keep working (and, for example, allow them to `terraform destroy` any
  infra they had access to).

- If the user was a member of the `owner` team of your TFC organization, they can bypass SSO
  entirely and regain their access both via the UI and API.

This behaviour is working "as designed" by HashiCorp - presumably as a break-glass measure.
Check out their [SSO documentation] for more details.

If you use Okta as your IdP, and any of the above scenarios apply to you, this small CLI would help
you flag the user accounts which are de-provisioned in Okta, but are still active in your TFC
organization.

## Requirements

- API tokens for Okta and Terraform Cloud (or Enterprise) with access to list users.
  These can be provided via environment variables (see Usage).

## Installation

You can install _Terraform Cloud Okta Warden_ via [pip] from [PyPI]:

```console
$ pip install terraform-cloud-okta-warden
```

## Usage

```shell
❯ terraform-cloud-okta-warden --help

 Usage: terraform-cloud-okta-warden [OPTIONS] OKTA_TOKEN TFC_TOKEN

 Checks for existence of non-active Okta users in Terraform Cloud organization.
 Non-active users are those who are missing or de-provisioned in Okta.

╭─ Arguments ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *    okta_token      TEXT  Okta API token with access to list users [env var: OKTA_TOKEN] [default: None] [required]                                                            │
│ *    tfc_token       TEXT  Terraform Cloud token with access to list users [env var: TFC_TOKEN] [default: None] [required]                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ *  --okta-org-url              TEXT  Your Okta domain url (e.g. https://mycompany.okta.com) [default: None] [required]                                                          │
│ *  --tfc-org-name              TEXT  Terraform Cloud Organization name [default: None] [required]                                                                               │
│    --tfc-url                   TEXT  Defaults to Terraform Cloud, provide the URL if you use Terraform Enterprise [default: https://app.terraform.io]                           │
│    --version                                                                                                                                                                    │
│    --log-level                 TEXT  [default: INFO]                                                                                                                            │
│    --install-completion              Install completion for the current shell.                                                                                                  │
│    --show-completion                 Show completion for the current shell, to copy it or customize the installation.                                                           │
│    --help                            Show this message and exit.                                                                                                                │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [Apache 2.0 license][license],
_Terraform Cloud Okta Warden_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@schubergphilis]: https://github.com/schubergphilis
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/schubergphilis/cookiecutter-hypermodern-python
[file an issue]: https://github.com/ninadpage/terraform-cloud-okta-warden/issues
[pip]: https://pip.pypa.io/
[sso documentation]: https://developer.hashicorp.com/terraform/cloud-docs/users-teams-organizations/single-sign-on#enforced-access-policy-for-terraform-cloud-resources

<!-- github-only -->

[license]: https://github.com/ninadpage/terraform-cloud-okta-warden/blob/main/LICENSE
[contributor guide]: https://github.com/ninadpage/terraform-cloud-okta-warden/blob/main/CONTRIBUTING.md
