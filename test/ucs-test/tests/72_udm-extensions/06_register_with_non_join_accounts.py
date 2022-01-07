#!/usr/share/ucs-test/runner pytest-3
## desc: Register UDM extension with non-join-accounts
## tags: [udm-extensions,apptest]
## roles: [domaincontroller_master,domaincontroller_backup,domaincontroller_slave,memberserver]
## exposure: dangerous
## packages:
##   - univention-config
##   - univention-directory-manager-tools
##   - shell-univention-lib

from __future__ import print_function
from test_udm_extensions import temp_deb_pkg
from univention.testing.utils import wait_for_replication
from univention.testing.udm_extensions import (
	get_package_name,
	get_package_version,
	get_extension_name,
	get_extension_filename,
	get_join_script_buffer,
	get_extension_buffer,
	call_cmd,
	get_dn_of_extension_by_name,
	VALID_EXTENSION_TYPES
)
import pytest


@pytest.fixture
def user_password():
	return 'univention'


@pytest.fixture
def user_dn(udm, user_password):
	dn, username = udm.create_user(password=user_password)
	return dn


def _test_extension(extension_type, dn, password):
	package_name = get_package_name()
	package_version = get_package_version()
	extension_name = get_extension_name(extension_type)
	extension_filename = get_extension_filename(extension_type, extension_name)
	joinscript_buffer = get_join_script_buffer(extension_type, '/usr/share/%s/%s' % (package_name, extension_filename), version_start='5.0-0')
	extension_buffer = get_extension_buffer(extension_type, extension_name)

	with temp_deb_pkg(package_name, package_version, extension_type, extension_name) as package:
		# create package and install it
		package.create_join_script_from_buffer('66%s.inst' % package_name, joinscript_buffer)
		package.create_usr_share_file_from_buffer(extension_filename, extension_buffer)
		package.build()
		package.install()

		exitcode = call_cmd(['/usr/lib/univention-install/66%s.inst' % package_name, '--binddn', dn, '--bindpwd', password], fail_on_error=False)
		assert exitcode, 'ERROR: registerLDAPExtension() did not fail even if machine account is used'

		# wait until removed object has been handled by the listener
		wait_for_replication()

		dnlist = get_dn_of_extension_by_name(extension_type, extension_name)
		assert not dnlist, 'ERROR: Machine account is able to create UDM %s extension' % (extension_type,)


@pytest.mark.tags('udm-extensions', 'apptest')
@pytest.mark.roles('domaincontroller_master', 'domaincontroller_backup', 'domaincontroller_slave', 'memberserver')
@pytest.mark.exposure('dangerous')
@pytest.mark.parametrize('extension_type', VALID_EXTENSION_TYPES)
def test_register_with_non_join_accounts(udm, ucr, user_password, user_dn, extension_type):
	"""Register UDM extension with non-join-accounts"""
	_test_extension(extension_type, user_dn, user_password)
	_test_extension(extension_type, ucr.get('ldap/hostdn'), open('/etc/machine.secret', 'r').read())
