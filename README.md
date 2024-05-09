# Ansible Collection: HashiCorp Vault

[![Gitlab pipeline status (self-hosted)](https://git.dubzland.com/dubzland/ansible-collections/vault/badges/main/pipeline.svg)](https://git.dubzland.com/dubzland/ansible-collections/vault/pipelines?scope=all&page=1&ref=main)
[![Ansible Galaxy](https://img.shields.io/badge/dynamic/json?style=flat&label=galaxy&prefix=v&url=https://galaxy.ansible.com/api/v3/collections/dubzland/vault/&query=highest_version.version)](https://galaxy.ansible.com/ui/repo/published/dubzland/vault/)
[![Liberapay patrons](https://img.shields.io/liberapay/patrons/jdubz)](https://liberapay.com/jdubz/donate)
[![Liberapay receiving](https://img.shields.io/liberapay/receives/jdubz)](https://liberapay.com/jdubz/donate)

Installs and configures the [HashiCorp Vault][vault] secret managment service.

## Ansible version compatibility

This collection has been tested against following ansible-core versions:

- 2.14
- 2.15
- 2.16
- 2.17

Also tested against the current development version of `ansible-core`.

## Included content

### Roles

| Name                                          | Description                                               |
| --------------------------------------------- | --------------------------------------------------------- |
| [dubzland.vault.vault_install][vault_install] | Installs the Vault binary                                 |
| [dubzland.vault.vault_server][vault_server]   | Configures the Vault server system service                |
| [dubzland.vault.vault_init][vault_init]       | Performs initial initialization on the Vault installation |
| [dubzland.vault.vault_unseal][vault_unseal]   | Unseals the Vault                                         |

## Licensing

This collection is primarily licensed and distributed as a whole under the MIT License.

See [LICENSE](https://git.dubzland.com/dubzland/ansible-collections/vault/blob/main/LICENSE) for the full text.

## Author

- [Josh Williams](https://dubzland.com)

[vault]: https://www.hashicorp.com/products/vault
[vault_install]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_install_role.html
[vault_server]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_server_role.html
[vault_init]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_init_role.html
[vault_unseal]: https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_unseal_role.html
