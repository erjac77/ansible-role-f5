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

    monitor = mgmt.tm.gtm.monitor.tcps.tcp.load(
        name="my_tcp_monitor", partition="Common"
    )
    assert monitor.name == "my_tcp_monitor"
    assert monitor.partition == "Common"
    assert monitor.description == "My tcp monitor"
