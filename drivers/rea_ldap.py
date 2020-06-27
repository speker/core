# -*- coding: utf-8 -*-

from core.reapy import ReaPy


class ReaLdap(object):
    configurations = None

    def __init__(self):
        super(ReaLdap).__init__()
        self.configurations = ReaPy.configuration().get_configuration()['system']['rest_server']['ldap']

    def authenticate(self, domain, username, password):
        connection = self.connect(domain, False)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']
            results = conn.simple_bind_s(username + '@' + domain['iam_domain_name'], password)
            conn.unbind_s()
        except ReaPy.ldap().INVALID_CREDENTIALS as e:
            print(e)
            return {'success': False, 'error': 'ldap_invalid_credentials'}
        except ReaPy.ldap().LDAPError as ad:
            print(ad)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': results}

    def connect(self, domain, bind=True):
        print('con1')
        if domain['iam_domain_ldap_use_ssl'] is True:
            ReaPy.ldap().set_option(ReaPy.ldap().OPT_X_TLS_REQUIRE_CERT, ReaPy.ldap().OPT_X_TLS_NEVER)
            proto = 'ldaps'
        else:
            proto = 'ldap'
        try:
            conn = ReaPy.ldap().initialize(
                proto + '://' + domain['iam_domain_ldap_host_address'] + ':' + str(domain['iam_domain_ldap_host_port']))
            conn.set_option(ReaPy.ldap().OPT_NETWORK_TIMEOUT, self.configurations['time_out'])
            conn.protocol_version = self.configurations['protocol_version']
            conn.set_option(ReaPy.ldap().OPT_REFERRALS, 0)
            conn.set_option(ReaPy.ldap().OPT_DEBUG_LEVEL, 255)
            if bind is True:
                conn.simple_bind_s(domain['iam_domain_ldap_host_user'] + '@' + domain['iam_domain_name'],
                                   domain['iam_domain_ldap_host_password'])
        except ReaPy.ldap().INVALID_CREDENTIALS as e:
            print(e)
            return {'success': False, 'error': 'ldap_ic_err_100', 'status': 417}
        except ReaPy.ldap().SERVER_DOWN as e:
            print(e)
            return {'success': False, 'error': 'ldap_cf_err_101', 'status': 417}
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}
        print('con2',conn)
        return {'success': True, 'data': conn}

    @staticmethod
    def check_user(domain, account_name, sid=None):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            base = []
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            # for ou_key in organization_unit:
            #     base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            criteria = "(&(objectClass=user)(sAMAccountName=" + account_name + ")"
            if sid is not None:
                criteria += "(objectSid="+sid+")"
            criteria += ")"
            conn = connection['data']
            result = conn.search_s(base, ReaPy.ldap().SCOPE_SUBTREE, criteria)
            results = [entry for dn, entry in result if isinstance(entry, dict)]
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}
        if len(results) == 0:
            return {'success': True, 'data': results, 'error': 'ldap_ex_err_102', 'status': 417}
        else:
            return {'success': True, 'data': results}

    @staticmethod
    def add_user(domain, user_data):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']

            base = ['CN=' + user_data['user_domain_account_name']]
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            for ou_key in organization_unit:
                base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            principal_name = user_data['user_domain_account_name'] + '@' + domain['iam_domain_name']
            display_name = user_data['user_name'] + ' ' + user_data['user_surname']
            attrs = {'objectclass': [b'top', b'person', b'organizationalPerson', b'user'],
                     'sAMAccountName': str.encode(user_data['user_domain_account_name']),
                     'givenName': str.encode(user_data['user_name']), 'displayName': str.encode(display_name),
                     'sn': str.encode(user_data['user_surname']),
                     'telephoneNumber': str.encode(user_data['user_phone_number']),
                     'mobile': str.encode(user_data['user_mobile_number']), 'mail': str.encode(user_data['user_email']),
                     'title': str.encode(user_data['user_title']),
                     'department': str.encode(user_data['user_department']),
                     'company': str.encode(user_data['user_company']),
                     'userPrincipalName': str.encode(principal_name),
                     'description': b'Added By IAM-ReActor'}

            user_domain_data = ReaPy.ldap_mod_list().addModlist(attrs)
            conn.add_s(base, user_domain_data)
            password = ReaPy.hash().ldap_password_generator()
            password_value = '"{}"'.format(password).encode('utf-16-le')
            add_pass = [(ReaPy.ldap().MOD_REPLACE, 'unicodePwd', [password_value])]
            conn.modify_s(base, add_pass)

            mod_acct = [(ReaPy.ldap().MOD_REPLACE, 'userAccountControl', b'512')]
            conn.modify_s(base, mod_acct)
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': 'results'}

    @staticmethod
    def lock_user(domain, user_data):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']

            base = ['CN=' + user_data]
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            for ou_key in organization_unit:
                base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            mod_acct = [(ReaPy.ldap().MOD_REPLACE, 'userAccountControl', b'514')]
            conn.modify_s(base, mod_acct)
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': 'results'}

    @staticmethod
    def unlock_user(domain, user_data):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']

            base = ['CN=' + user_data]
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            for ou_key in organization_unit:
                base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            mod_acct = [(ReaPy.ldap().MOD_REPLACE, 'userAccountControl', b'512')]
            conn.modify_s(base, mod_acct)
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': 'results'}

    @staticmethod
    def reset_password_user(domain, user_data):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']
            base = ['CN=' + user_data['user_domain_account_name']]
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            for ou_key in organization_unit:
                base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            password_value = '"{}"'.format(user_data['user_domain_new_password']).encode('utf-16-le')
            add_pass = [(ReaPy.ldap().MOD_REPLACE, 'unicodePwd', [password_value])]
            conn.modify_s(base, add_pass)
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': 'results'}

    @staticmethod
    def search_user(domain, search_username, attr_key=None, attr_value=None):
        connection = ReaLdap().connect(domain)

        if connection['success'] is False:
            return connection
        try:
            base = []
            domain_name = domain['iam_domain_name'].split('.')
            organization_unit = domain['iam_domain_organization_unit'].split('.')
            # for ou_key in organization_unit:
            #     base.append('OU=' + ou_key)
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            criteria = "(&(objectClass=user)(sAMAccountName=" + search_username + ")"
            if attr_key is not None and attr_value is not None:
                criteria += "("+attr_key+"="+attr_value+")"
            criteria += ")"
            conn = connection['data']
            result = conn.search_s(base, ReaPy.ldap().SCOPE_SUBTREE, criteria)
            results = [entry for dn, entry in result if isinstance(entry, dict)]
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}
        if len(results) == 0:
            return {'success': True, 'data': results, 'error': 'ldap_ex_err_102', 'status': 417}
        else:
            return {'success': True, 'data': results}

    def update_attribute(self, domain, username, attr_key, attr_value):
        connection = ReaLdap().connect(domain, True)

        if connection['success'] is False:
            return connection
        try:
            conn = connection['data']
            base = ['CN=' + username]
            base.append('CN=Users')
            domain_name = domain['iam_domain_name'].split('.')
            for dc_key in domain_name:
                base.append('DC=' + dc_key)
            base = ','.join(base)
            mod_acct = [(ReaPy.ldap().MOD_REPLACE, attr_key, attr_value)]
            conn.modify_s(base, mod_acct)
            conn.unbind_s()
        except ReaPy.ldap().LDAPError as e:
            print(e)
            return {'success': False, 'error': 'ldap_ex_err_102', 'status': 417}

        return {'success': True, 'data': 'results'}
