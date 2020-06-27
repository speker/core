# -*- coding: utf-8 -*-
import ldap


class Ldap:

    def __init__(self):
        super(Ldap, self).__init__()

    @staticmethod
    def authenticate(address, username, password):
        conn = ldap.initialize('ldap://' + address)
        conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 5)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        try:
            result = conn.simple_bind_s(username, password)
        except ldap.INVALID_CREDENTIALS:
            return {'success': False, 'error': 'ldap_invalid_credentials'}
        except ldap.SERVER_DOWN:
            return {'success': False, 'error': 'ldap_server_down'}
        except ldap.LDAPError as e:
            return {'success': False, 'error': 'ldap_exception: ' + str(e)}
        finally:
            conn.unbind_s()
        return {'success': True, 'data': result}


