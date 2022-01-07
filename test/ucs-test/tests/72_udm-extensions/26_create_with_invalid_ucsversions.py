#!/usr/share/ucs-test/runner pytest-3
## desc: Create full UDM extension objects via CLI
## tags: [udm-ldapextensions,apptest]
## roles: [domaincontroller_master,domaincontroller_backup,domaincontroller_slave,memberserver]
## exposure: dangerous
## packages:
##   - univention-directory-manager-tools

from __future__ import print_function
import univention.testing.udm as udm_test
from univention.testing.utils import fail
from univention.testing.strings import random_name, random_version, random_ucs_version
from univention.testing.udm_extensions import (
	get_package_name,
	get_package_version,
	get_extension_name,
	get_extension_filename,
	get_extension_buffer,
	VALID_EXTENSION_TYPES,
)
import bz2
import pytest
import base64

@pytest.mark.tags('udm-ldapextensions', 'apptest')
@pytest.mark.roles('domaincontroller_master', 'domaincontroller_backup', 'domaincontroller_slave', 'memberserver')
@pytest.mark.exposure('dangerous')
@pytest.mark.parametrize('extension_type', VALID_EXTENSION_TYPES)
def test_create_with_invalid_ucsversions(udm, extension_type):
	"""Create full UDM extension objects via CLI"""
	for extension_type in VALID_EXTENSION_TYPES:
		print('========================= TESTING EXTENSION %s =============================' % extension_type)
		for (version_start, version_end) in (
			(random_ucs_version(max_major=2), random_name()),
			(random_name(), random_ucs_version(min_major=5)),
			(random_name(), random_name())
		):
			extension_name = get_extension_name(extension_type)
			extension_filename = get_extension_filename(extension_type, extension_name)
			extension_buffer = get_extension_buffer(extension_type, extension_name)

			package_name = get_package_name()
			package_version = get_package_version()
			app_id = '%s-%s' % (random_name(), random_version())

			try:
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
					active='FALSE'
				)
				fail('Extension %s has been created with invalid UCS version (ucsversionstart=%r ucsversionend=%r)' % (extension_type, version_start, version_end))
			except udm_test.UCSTestUDM_CreateUDMObjectFailed:
				pass
