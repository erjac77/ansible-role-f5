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

    dc = mgmt.tm.gtm.datacenters.datacenter.load(name="my_datacenter")
    assert dc.name == "my_datacenter"
    assert dc.description == "My datacenter"
    assert dc.contact == "admin@localhost"
    assert dc.location == "Somewhere"
