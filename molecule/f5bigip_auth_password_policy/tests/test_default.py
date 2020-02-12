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

    policy = mgmt.tm.auth.password_policy.load()
    assert policy.expirationWarning == 5
    assert policy.maxDuration == 90
    assert policy.maxLoginFailures == 3
    assert policy.minDuration == 30
    assert policy.minimumLength == 8
    assert policy.passwordMemory == 1
    assert policy.policyEnforcement == "enabled"
    assert policy.requiredLowercase == 2
    assert policy.requiredNumeric == 1
    assert policy.requiredSpecial == 1
    assert policy.requiredUppercase == 2
