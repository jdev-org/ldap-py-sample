"""
Compat helper so legacy imports like ``import ldap_connection`` continue to work
after packaging. Delegates to ``ldap_actions.ldap_connection``.
"""

from ldap_actions.ldap_connection import get_connection

__all__ = ["get_connection"]
