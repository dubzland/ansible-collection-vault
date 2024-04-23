# Ansible Role: HashiCorp Vault initialization

Initializes a HashiCorp Vault secret management server installation.

## Usage

Install the collection locally, either via `requirements.yml`, or manually:

```bash
ansible-galaxy collection install dubzland.vault
```

Then apply the role using the following playbook:

```yaml
---
- hosts: vault_hosts

  collections:
    - dubzland.vault

  roles:
    - role: vault_init
```

When complete, the root key will be present locally in the `vault-tokens`
directory.

## Documentation

Role documentation is available at <https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_init_role.html>.

## License

MIT

## Author

- [Josh Williams](https://dubzland.com)
