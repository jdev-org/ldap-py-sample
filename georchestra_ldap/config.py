from __future__ import annotations

import os
from dataclasses import dataclass


def _bool_env(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class LdapSettings:
    """
    Configuration holder used by :class:`GeorchestraLdapClient`.

    The ``from_env`` helper reads the same variable names as the former
    ``config.py`` file so existing deployments can keep their environment.
    """

    server: str = "ldap://localhost"
    port: int = 389
    use_ssl: bool = False
    user_dn: str = "cn=admin,dc=georchestra,dc=org"
    password: str = "secret"
    users_dn: str = "ou=users"
    pending_users_dn: str = "ou=pendingusers"
    org_dn: str = "ou=orgs"
    role_dn: str = "ou=roles"
    search_base: str = "dc=georchestra,dc=org"
    mail_attribute: str = "mail"
    default_role_cn: str = "USER"
    default_org_cn: str = "C2C"

    @classmethod
    def from_env(cls) -> "LdapSettings":
        """
        Build a settings object using environment variables.

        Supported variables mirror the legacy ``config.py`` names:
        ``LDAP_SERVER``, ``LDAP_PORT``, ``LDAP_USE_SSL``, ``LDAP_USER_DN``,
        ``LDAP_PASSWORD``, ``LDAP_USERS_DN``, ``LDAP_PENDING_USERS_DN``,
        ``LDAP_ORG_DN``, ``LDAP_ROLE_DN``, ``LDAP_SEARCH_BASE``,
        ``LDAP_MAIL_ATTRIBUTE``, ``LDAP_DEFAULT_ROLE_CN``, ``LDAP_DEFAULT_ORG_CN``.
        """

        return cls(
            server=os.getenv("LDAP_SERVER", cls.server),
            port=int(os.getenv("LDAP_PORT", cls.port)),
            use_ssl=_bool_env("LDAP_USE_SSL", cls.use_ssl),
            user_dn=os.getenv("LDAP_USER_DN", cls.user_dn),
            password=os.getenv("LDAP_PASSWORD", cls.password),
            users_dn=os.getenv("LDAP_USERS_DN", cls.users_dn),
            pending_users_dn=os.getenv("LDAP_PENDING_USERS_DN", cls.pending_users_dn),
            org_dn=os.getenv("LDAP_ORG_DN", cls.org_dn),
            role_dn=os.getenv("LDAP_ROLE_DN", cls.role_dn),
            search_base=os.getenv("LDAP_SEARCH_BASE", cls.search_base),
            mail_attribute=os.getenv("LDAP_MAIL_ATTRIBUTE", cls.mail_attribute),
            default_role_cn=os.getenv("LDAP_DEFAULT_ROLE_CN", cls.default_role_cn),
            default_org_cn=os.getenv("LDAP_DEFAULT_ORG_CN", cls.default_org_cn),
        )

    @property
    def users_base_dn(self) -> str:
        return f"{self.users_dn},{self.search_base}"

    @property
    def pending_users_base_dn(self) -> str:
        return f"{self.pending_users_dn},{self.search_base}"

    @property
    def roles_base_dn(self) -> str:
        return f"{self.role_dn},{self.search_base}"

    @property
    def orgs_base_dn(self) -> str:
        return f"{self.org_dn},{self.search_base}"
