#!/usr/share/ucs-test/runner pytest-3
## desc: Create full UDM extension objects via CLI
## tags: [udm-ldapextensions,apptest]
## roles: [domaincontroller_master,domaincontroller_backup,domaincontroller_slave,memberserver]
## exposure: dangerous
## packages:
##   - univention-directory-manager-tools

from __future__ import print_function
import bz2
import base64

import pytest

import univention.testing.udm as udm_test
from univention.config_registry import ConfigRegistry
from univention.testing.utils import verify_ldap_object
from univention.testing.strings import random_name, random_version, random_ucs_version
from univention.testing.udm_extensions import (
	get_package_name,
	get_package_version,
	get_extension_name,
	get_extension_filename,
	get_extension_buffer,
	VALID_EXTENSION_TYPES,
)

class Test_UDMExtension(object):
	@pytest.mark.tags('udm-ldapextensions', 'apptest')
	@pytest.mark.roles('domaincontroller_master', 'domaincontroller_backup', 'domaincontroller_slave', 'memberserver')
	@pytest.mark.exposure('dangerous')
	@pytest.mark.parametrize('extension_type',VALID_EXTENSION_TYPES)
	def test_20_create_via_udm_cli(self, udm,extension_type, ucr):
		"""Create full UDM extension objects via CLI"""
		print('========================= TESTING EXTENSION %s =============================' % extension_type)
		for active in ['TRUE', 'FALSE']:
			extension_name = get_extension_name(extension_type)
			extension_filename = get_extension_filename(extension_type, extension_name)
			extension_buffer = get_extension_buffer(extension_type, extension_name)
			package_name = get_package_name()
			package_version = get_package_version()
			app_id = '%s-%s' % (random_name(), random_version())
			version_start = random_ucs_version(max_major=2)
			version_end = random_ucs_version(min_major=5)
			dn = udm.create_object(
				'settings/udm_%s' % extension_type,
				name=extension_name,
				data=base64.b64encode(bz2.compress(extension_buffer)),
				filename=extension_filename,
				packageversion=package_version,
				appidentifier=app_id,
				package=package_name,
				ucsversionstart=version_start,
				ucsversionend=version_end,
				active=active,
				position='cn=udm_%s,cn=univention,%s' % (extension_type, ucr['ldap/base'])
			)
			verify_ldap_object(dn, {
				'cn': [extension_name],
				'univentionUDM%sFilename' % extension_type.capitalize(): [extension_filename],
				'univentionOwnedByPackage': [package_name],
				'univentionObjectType': ['settings/udm_%s' % extension_type],
				'univentionOwnedByPackageVersion': [package_version],
				'univentionUDM%sData' % extension_type.capitalize(): [bz2.compress(extension_buffer)],
				'univentionAppIdentifier': [app_id],
				'univentionUCSVersionStart': [version_start],
				'univentionUCSVersionEnd': [version_end],
			})
