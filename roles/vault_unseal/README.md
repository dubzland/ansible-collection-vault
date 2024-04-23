# Ansible Role: HashiCorp Vault unseal

Unseals a HashiCorp Vault secret management server installation.

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
    - role: vault_unseal
```

This assumes the root and unseal keys are present locally in the `vault-tokens`
directory.

## Documentation

Role documentation is available at <https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_unseal_role.html>.

## License

MIT

## Author

- [Josh Williams](https://dubzland.com)
