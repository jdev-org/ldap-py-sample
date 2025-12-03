#!/usr/bin/env python3

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ldap3 import MODIFY_DELETE
from ldap_connection import get_connection
import config


def remove_role(email: str, role_cn: str):
    conn = get_connection()

    # 1) Trouver l'utilisateur par email
    conn.search(
        search_base=config.LDAP_SEARCH_BASE,
        search_filter=f"({config.LDAP_MAIL_ATTRIBUTE}={email})",
        search_scope="SUBTREE",
        attributes=[]  # important : ne pas demander "dn"
    )

    if not conn.entries:
        print(f"User not found: {email}")
        return

    user_dn = conn.entries[0].entry_dn
    print(f"User DN found: {user_dn}")

    # 2) Construire le DN du rôle
    role_dn = f"cn={role_cn},{config.LDAP_ROLE_DN},{config.LDAP_SEARCH_BASE}"

    # 3) Vérifier que le rôle existe
    conn.search(
        search_base=f"{config.LDAP_ROLE_DN},{config.LDAP_SEARCH_BASE}",
        search_filter=f"(cn={role_cn})",
        attributes=["member"]
    )

    if not conn.entries:
        print(f"Role not found: {role_cn}")
        return

    print(f"Removing user from role: {role_dn}")

    # 4) Supprimer le user du rôle
    try:
        conn.modify(
            role_dn,
            {"member": [(MODIFY_DELETE, [user_dn])]}
        )
        print("Role removal successful.")
    except Exception as e:
        print("Error removing user from role:", e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python remove_user_role.py <email> <role_cn>")
        sys.exit(1)

    remove_role(sys.argv[1], sys.argv[2])
