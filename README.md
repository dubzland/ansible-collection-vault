# Ansible Collection: HashiCorp Vault

[![Gitlab pipeline][pipeline-badge]][pipeline-url]
[![Gitlab coverage][coverage-badge]][coverage-url]
[![Galaxy Version][galaxy-badge]][galaxy-url]
[![license][license-badge]][license-url]
[![Liberapay patrons][liberapay-patrons-badge]][liberapay-url]
[![Liberapay receiving][liberapay-receives-badge]][liberapay-url]

Installs and configures the [HashiCorp Vault][vault] secret managment service.

## Ansible version compatibility

This collection has been tested against following ansible-core versions:

- 2.16
- 2.17
- 2.18

Also tested against the current development version of `ansible-core`.

## Included content

### Roles

| Name                                          | Description                                               |
| --------------------------------------------- | --------------------------------------------------------- |
| [dubzland.vault.vault_install][vault_install] | Installs the Vault binary                                 |
| [dubzland.vault.vault_server][vault_server]   | Configures the Vault server system service                |
| [dubzland.vault.vault_init][vault_init]       | Performs initial initialization on the Vault installation |
| [dubzland.vault.vault_unseal][vault_unseal]   | Unseals the Vault                                         |

### Modules

| Name                                                  | Description                          |
| ----------------------------------------------------- | -------------------------------------|
| [dubzland.vault.vault_auth_method][vault_auth_method] | Manages Vault Authentication methods |

## Licensing

This collection is primarily licensed and distributed as a whole under the MIT License.

See [LICENSE](https://git.dubzland.com/dubzland/ansible-collections/vault/blob/main/LICENSE) for the full text.

## Author

- [Josh Williams](https://dubzland.com)

[pipeline-badge]: https://img.shields.io/gitlab/pipeline-status/dubzland%2Fansible-collections%2Fvault?gitlab_url=https%3A%2F%2Fgit.dubzland.com&branch=main&style=flat-square&logo=gitlab
[pipeline-url]: https://git.dubzland.com/dubzland/ansible-collections/vault/pipelines?scope=all&page=1&ref=main
[coverage-badge]: https://img.shields.io/gitlab/pipeline-coverage/dubzland%2Fansible-collections%2Fvault?gitlab_url=https%3A%2F%2Fgit.dubzland.com&branch=main&style=flat-square&logo=gitlab
[coverage-url]: https://git.dubzland.com/dubzland/ansible-collections/vault/pipelines?scope=all&page=1&ref=main
[galaxy-badge]: https://img.shields.io/badge/dynamic/json?style=flat-square&label=galaxy&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/dubzland/vault/&query=highest_version.version
[galaxy-url]: https://galaxy.ansible.com/ui/repo/published/dubzland/vault/
[license-badge]: https://img.shields.io/gitlab/license/dubzland%2Fcontainer-images%2Fci-python?gitlab_url=https%3A%2F%2Fgit.dubzland.com&style=flat-square
[license-url]: https://git.dubzland.com/dubzland/container-images/ci-python/-/blob/main/LICENSE
[liberapay-patrons-badge]: https://img.shields.io/liberapay/patrons/jdubz?style=flat-square&logo=liberapay
[liberapay-receives-badge]: https://img.shields.io/liberapay/receives/jdubz?style=flat-square&logo=liberapay
[liberapay-url]: https://liberapay.com/jdubz/donate
[vault]: https://www.hashicorp.com/products/vault
[vault_install]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_install_role.html
[vault_server]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_server_role.html
[vault_init]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_init_role.html
[vault_unseal]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_unseal_role.html
[vault_auth_method]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_auth_method_module.html
