from ansible_vault import Vault
from f5.bigip import ManagementRoot


def test_default(host):
    vars = host.ansible.get_variables()
    vault_pass = open("../../molecule/.vault_pass", "r").read().replace("\n", "")
    vault = Vault(vault_pass)
    decrypted_host = vault.load(vars["ansible_host"]["__ansible_vault"])
    decrypted_user = vault.load(vars["http_user"]["__ansible_vault"])
    decrypted_pass = vault.load(vars["http_pass"]["__ansible_vault"])
    mgmt = ManagementRoot(decrypted_host, decrypted_user, decrypted_pass)

    decrypted_device_name = vault.load(vars["device_name"]["__ansible_vault"])
    decrypted_device_internal_ip = vault.load(
        vars["device_internal_ip"]["__ansible_vault"]
    )
    device = mgmt.tm.cm.devices.device.load(name=decrypted_device_name)
    assert device.name == decrypted_device_name
    assert device.comment == "My lab device"
    assert device.configsyncIp == decrypted_device_internal_ip
    assert device.contact == "admin@localhost"
    assert device.description == "My device"
    assert device.haCapacity == 10
    assert device.location == "Central Office"
