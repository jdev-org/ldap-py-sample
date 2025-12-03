# Repository Overview *ldap-py*

This repository contains a collection of Python scripts designed to easily manage users, roles, and organizations in a geOrchestra-compatible LDAP directory.  
The goal is to provide a simple, consistent, and automatable toolkit for administering LDAP without relying on heavy interfaces or manual commands.

## Main Features

- **User creation** with the correct geOrchestra objectClasses  
- **Automatic assignment** of the `USER` role and the `C2C` organization
- **Account activation** (pending → users)
- **Role creation and assignment**
- **Organization creation**
- **Full retrieval** of user information
- **Targeted retrieval** of user roles
- **Clean user deletion** (removal from all groups)
- Modular architecture: all scripts share a common LDAP connection handler

## Purpose

To make LDAP administration accessible and automatable by providing standalone, readable, composable scripts that remain fully compatible with geOrchestra, without requiring deep LDAP knowledge.

Each script can be used individually or integrated into CI/CD pipelines or internal automation tools.

# Summary of LDAP Scripts

| Script | Function |
|--------|----------|
| **read_user_infos.py** | Searches for a user by email and displays information: DN, uid, cn, mail, and all groups (`memberOf`). |
| **read_user_roles.py** | Displays only the LDAP roles of a user (entries under `ou=roles`). |
| **create_user.py** | Creates a user in `ou=pendingusers` using proper geOrchestra objectClasses, generates an SSHA password, and automatically assigns the `USER` role and the `C2C` organization. |
| **moderate_user.py** | Activates a user by moving them from `ou=pendingusers` to `ou=users` without altering roles or organization. |
| **add_user_role.py** | Adds a role (LDAP group) to a user by inserting their DN into the role’s `member` attribute. |
| **create_role.py** | Creates a new LDAP role in `ou=roles` if it does not already exist. |
| **create_org.py** | Creates a new LDAP organization in `ou=orgs` if it does not already exist. |
| **delete_user.py** | Deletes a user: removes them from all roles and organizations, then deletes the LDAP entry. |

# LDAP Command Summary Table

| Action | Command |
|--------|---------|
| Read user information | `python ldap_actions/read_user_infos.py utest2@utest.fr` |
| Read user roles | `python ldap_actions/read_user_roles.py utest2@utest.fr` |
| Create a user (pending + USER + C2C) | `python ldap_actions/create_user.py utest2 utest2@utest.fr Test User2 MySecretPass123` |
| Activate a user (pending → users) | `python ldap_actions/moderate_user.py utest2@utest.fr` |
| Add a role to a user | `python ldap_actions/add_user_role.py "uid=utest2,ou=users,dc=georchestra,dc=org" SUPERUSER` |
| Create a role if it does not exist | `python ldap_actions/create_role.py MYCUSTOMROLE` |
| Create an organization if it does not exist | `python ldap_actions/create_org.py MYORG "My Organization"` |
| Delete a user | `python ldap_actions/delete_user.py utest2@utest.fr` |
