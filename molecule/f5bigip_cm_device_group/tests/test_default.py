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

    dg = mgmt.tm.cm.device_groups.device_group.load(name="my_device_group")
    assert dg.name == "my_device_group"
    assert dg.description == "My device group"
    devices = dg.devices_s.get_collection()
    assert len(devices) == 1
    decrypted_device_name = vault.load(vars["device_name"]["__ansible_vault"])
    assert devices[0].name == decrypted_device_name
