# Ansible Role: HashiCorp Vault Server

Configures HashiCorp Vault server as a system service.

## Usage

Install the collection locally, either via `requirements.yml`, or manually:

```bash
ansible-galaxy collection install dubzland.vault
```

Then apply the role using the following playbook:

```yaml
---
- hosts: vault_servers

  collections:
    - dubzland.vault

  roles:
    - role: vault_install
    - role: vault_server
```

## Documentation

Role documentation is available at <https://docs.dubzland.io/ansible-collections/collections/dubzland/vault/vault_install_role.html>.

## License

MIT

## Author

- [Josh Williams](https://dubzland.com)

