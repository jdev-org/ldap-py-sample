# georchestra-ldap-py

Thin Python wrapper around the legacy `ldap_actions` scripts used with geOrchestra LDAP directories. Installable via pip, configurable via environment variables, and consumable as a small API.

## Quick install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install .
# or directly from git
# pip install "git+https://github.com/jdev-org/georchestra-ldap-py.git"
```

## Configure (env vars)

All settings are read via `LdapSettings.from_env()` and applied to the legacy `config.py` in memory. Override as needed:

```
LDAP_SERVER, LDAP_PORT, LDAP_USE_SSL,
LDAP_USER_DN, LDAP_PASSWORD,
LDAP_USERS_DN, LDAP_PENDING_USERS_DN, LDAP_ORG_DN, LDAP_ROLE_DN,
LDAP_SEARCH_BASE, LDAP_MAIL_ATTRIBUTE,
LDAP_DEFAULT_ROLE_CN, LDAP_DEFAULT_ORG_CN
```

## Example usage

```python
from georchestra_ldap import GeorchestraLdapClient, LdapSettings

client = GeorchestraLdapClient(LdapSettings.from_env())
client.create_role("FOO")
client.create_user("alice", "alice@example.org", "Alice", "Example", "Pwd123!")
client.moderate_user("alice@example.org")
client.add_user_role("alice@example.org", "FOO")
client.read_user_roles("alice@example.org")
```
