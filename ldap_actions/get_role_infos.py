#!/usr/bin/env python3

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ldap_connection import get_connection
import config


def get_role_infos(role_cn: str):
    """
    Return the ldap3 entry for a role searched by cn and print its attributes/members.
    """
    conn = get_connection()

    conn.search(
        search_base=f"{config.LDAP_ROLE_DN},{config.LDAP_SEARCH_BASE}",
        search_filter=f"(cn={role_cn})",
        attributes=["cn", "description", "member"],
    )

    if not conn.entries:
        print(f"Role not found: {role_cn}")
        return None

    role = conn.entries[0]

    print("=== Role Information ===")
    print(f"DN: {role.entry_dn}")
    print(f"cn: {role.cn.value if 'cn' in role else None}")
    print(f"description: {role.description.value if 'description' in role else None}")

    print("\nMembers:")
    if "member" in role:
        for m in role.member.values:
            print(f" - {m}")
    else:
        print("No members")

    return role


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_role_infos.py <ROLE_CN>")
        sys.exit(1)

    get_role_infos(sys.argv[1])
