#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ldap_connection import get_connection
import config


def get_user_infos(email: str):
    """
    Return the ldap3 entry for a user searched by email and print its main attributes.
    """
    conn = get_connection()

    conn.search(
        search_base=config.LDAP_SEARCH_BASE,
        search_filter=f"({config.LDAP_MAIL_ATTRIBUTE}={email})",
        attributes=["cn", "uid", "mail", "memberOf"],
    )

    if not conn.entries:
        print("User not found.")
        return None

    user = conn.entries[0]

    print("=== User Information ===")
    print(f"DN: {user.entry_dn}")
    print(f"uid: {user.uid.value if 'uid' in user else None}")
    print(f"cn: {user.cn.value if 'cn' in user else None}")
    print(f"mail: {user.mail.value if 'mail' in user else None}")

    print("\nGroups (memberOf):")
    if "memberOf" in user:
        for m in user.memberOf.values:
            print(f" - {m}")
    else:
        print("No groups")

    return user


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_user_infos.py <email>")
        sys.exit(1)

    get_user_infos(sys.argv[1])
