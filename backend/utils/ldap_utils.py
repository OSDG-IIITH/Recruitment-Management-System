"""
LDAP utils copied over from https://github.com/IMS-IIITH/backend/blob/master/utils/ldap_utils.py,
courtesy of https://github.com/bhavberi
"""

import ldap
from os import getenv

# LDAP server configuration
LDAP_SERVER = getenv("LDAP_SERVER", "ldap://localhost:389")
BASE_DN = getenv("BASE_DN", "dc=example,dc=com")


def get_user_by_email(email):
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s()

        search_filter = f"(mail={email})"
        results = conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE, search_filter)

        if results:
            _, user_entry = results[0]
            return user_entry
        else:
            # User not found
            return None
    except ldap.LDAPError as e:
        # print(f'LDAP Error: {e}')
        return None


def authenticate_user(email, password):
    try:
        conn = ldap.initialize(LDAP_SERVER)
        conn.simple_bind_s()

        search_filter = f"(mail={email})"
        results = conn.search_s(BASE_DN, ldap.SCOPE_SUBTREE, search_filter)

        if results:
            dn, user_entry = results[0]
            if conn.simple_bind_s(dn, password):
                # Authentication successful
                # display_name = user_entry.get('cn', [''])[0]
                # print(user_entry["uid"][0].decode())
                return True, user_entry
        else:
            # User not found
            return False, None
    except ldap.LDAPError as e:
        # print(f'LDAP Error: {e}')
        return False, None

    return False, None


if __name__ == "__main__":
    print(get_user_by_email("kritin.maddireddy@students.iiit.ac.in"))
