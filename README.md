# Ansible Role for F5 systems

[![Made with](https://img.shields.io/badge/made%20with-python-blue.svg)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)
[![Ansible Quality Score](https://img.shields.io/ansible/quality/46429)](https://galaxy.ansible.com/erjac77/docker)
[![Ansible Role](https://img.shields.io/ansible/role/46429)](https://galaxy.ansible.com/erjac77/docker)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)

An Ansible module to perform specific operational and configuration tasks on F5 systems.
Over 190 components supported (and counting).

Supported F5 systems:

- BIG-IP
- BIG-IQ
- iWorkflow

## Requirements

- Ansible >= 2.8.0 (ansible)
- F5 Python SDK >= 3.0.21 (f5-sdk)
- Deep Difference >= 4.2.0 (deepdiff)
- Requests: HTTP for Humans >= 2.22.0 (requests)

## Installation

### 1. Install requirements

```shell
pip3 install "ansible>=2.8.0"
pip3 install "deepdiff>=4.2.0"
pip3 install "f5-sdk>=3.0.21"
pip3 install "requests>=2.22.0"
```

### 2. Install F5 Role from Ansible Galaxy

```shell
ansible-galaxy install erjac77.f5
```

## Example Playbook

```yaml
- hosts: bigips
  connection: local
  roles:
    - erjac77.f5

  tasks:
    - name: Create LTM Pool
      f5bigip_ltm_pool:
        provider:
          server: "{{ inventory_hostname }}"
          server_port: 443
          user: admin
          password: admin
          validate_certs: false
        name: my_pool
        partition: Common
        description: My Pool
        load_balancing_mode: least-connections-members
        state: present
```

You'll find more examples in the [Wiki](https://github.com/erjac77/ansible-role-f5/wiki/Playbook-Examples).

## License

Apache 2.0

## Author Information

- Eric Jacob ([@erjac77](https://github.com/erjac77))

### Contributors

- Gabriel Fortin ([@GabrielFortin](https://github.com/GabrielFortin))
