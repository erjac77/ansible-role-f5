from ansible_vault import Vault
from deepdiff import DeepDiff
from f5.bigip import ManagementRoot


def test_default(host):
    vars = host.ansible.get_variables()
    vault_pass = open("../../molecule/.vault_pass", "r").read().replace("\n", "")
    vault = Vault(vault_pass)
    decrypted_host = vault.load(vars["ansible_host"]["__ansible_vault"])
    decrypted_user = vault.load(vars["http_user"]["__ansible_vault"])
    decrypted_pass = vault.load(vars["http_pass"]["__ansible_vault"])
    mgmt = ManagementRoot(decrypted_host, decrypted_user, decrypted_pass)

    user = mgmt.tm.auth.users.user.load(name="user1")
    assert user.name == "user1"
    assert user.description == "User 1"
    partition_access = [
        {"name": "Common", "role": "guest"},
        {"name": "Test", "role": "operator"},
    ]
    assert not DeepDiff(
        partition_access,
        user.partitionAccess,
        exclude_regex_paths={r"root\[\d+\]\['nameReference'\]"},
    )
