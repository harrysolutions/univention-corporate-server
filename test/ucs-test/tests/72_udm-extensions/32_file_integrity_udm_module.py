#!/usr/share/ucs-test/runner pytest-3
## desc: Register and deregister UDM extension via joinscript
## tags: [udm-extensions,apptest]
## roles: [domaincontroller_master,domaincontroller_backup,domaincontroller_slave,memberserver]
## exposure: dangerous
## packages:
##   - univention-config
##   - univention-directory-manager-tools
##   - shell-univention-lib

from __future__ import print_function
import os
import hashlib
import difflib

from test_udm_extensions import temp_deb_pkg
from univention.testing.utils import wait_for_replication
import pytest
from univention.testing.udm_extensions import (
	get_package_name,
	get_package_version,
	get_extension_name,
	get_extension_filename,
	get_extension_buffer,
	get_unjoin_script_buffer,
	get_join_script_buffer,
	call_join_script,
	get_dn_of_extension_by_name,
	call_unjoin_script,
	get_absolute_extension_filename
)

TEST_DATA = (
	('umcregistration', '32_file_integrity_udm_module.xml', '/usr/share/univention-management-console/modules/udm-%s.xml'),
	('icon', '32_file_integrity_udm_module-16.png', '/usr/share/univention-management-console-frontend/js/dijit/themes/umc/icons/16x16/udm-%s.png'),
	('icon', '32_file_integrity_udm_module-50.png', '/usr/share/univention-management-console-frontend/js/dijit/themes/umc/icons/50x50/udm-%s.png'),
	('messagecatalog', 'it.mo', '/usr/share/locale/it/LC_MESSAGES/univention-admin-handlers-%s.mo'),
	('messagecatalog', 'de.mo', '/usr/share/locale/de/LC_MESSAGES/univention-admin-handlers-%s.mo'),
	('messagecatalog', 'es.mo', '/usr/share/locale/es/LC_MESSAGES/univention-admin-handlers-%s.mo'),
)


@pytest.mark.tags('udm-extensions', 'apptest')
@pytest.mark.roles('domaincontroller_master', 'domaincontroller_backup', 'domaincontroller_slave', 'memberserver')
@pytest.mark.exposure('dangerous')
def test_file_integrity_udm_module():
	"""Register and deregister UDM extension via joinscript"""
	extension_type = 'module'
	package_name = get_package_name()
	package_version = get_package_version()
	extension_name = get_extension_name(extension_type)
	extension_filename = get_extension_filename(extension_type, extension_name)

	options = {}
	buffers = {}
	for option_type, filename, target_filename in TEST_DATA:
		buffers[filename] = open('/usr/share/ucs-test/72_udm-extensions/%s' % filename, 'r').read()
		options.setdefault(option_type, []).append('/usr/share/%s/%s' % (package_name, filename))

	joinscript_buffer = get_join_script_buffer(extension_type, '/usr/share/%s/%s' % (package_name, extension_filename), options=options, version_start='5.0-0')
	unjoinscript_buffer = get_unjoin_script_buffer(extension_type, extension_name, package_name)
	extension_buffer = get_extension_buffer(extension_type, extension_name)

	print(joinscript_buffer)

	with temp_deb_pkg(package_name, package_version, extension_type, extension_name) as package:
		# create package and install it
		package.create_join_script_from_buffer('66%s.inst' % package_name, joinscript_buffer)
		package.create_unjoin_script_from_buffer('66%s-uninstall.uinst' % package_name, unjoinscript_buffer)
		package.create_usr_share_file_from_buffer(extension_filename, extension_buffer)
		for fn, data in buffers.items():
			package.create_usr_share_file_from_buffer(fn, data)
		package.build()
		package.install()

		call_join_script('66%s.inst' % package_name)

		# wait until removed object has been handled by the listener
		wait_for_replication()

		dnlist = get_dn_of_extension_by_name(extension_type, extension_name)
		assert dnlist, 'ERROR: cannot find UDM extension object with cn=%s in LDAP' % extension_name

		# check if registered file has been replicated to local system
		target_fn = get_absolute_extension_filename(extension_type, extension_filename)
		assert os.path.exists(target_fn), 'ERROR: target file %s does not exist' % target_fn

		# check if sha1(buffer) == sha1(file)
		hash_buffer = hashlib.sha1(extension_buffer).hexdigest()
		hash_file = hashlib.sha1(open(target_fn).read()).hexdigest()
		print('HASH BUFFER: %r' % hash_buffer)
		print('HASH FILE: %r' % hash_file)
		if hash_buffer != hash_file:
			print('\n'.join(difflib.context_diff(open(target_fn).read(), extension_buffer, fromfile='filename', tofile='buffer')))
			pytest.fail('ERROR: sha1 sums of file and BUFFER DIffer (fn=%s ; file=%s ; buffer=%s)' % (target_fn, hash_file, hash_buffer))

		for option_type, src_fn, filename in TEST_DATA:
			filename = filename % extension_name.replace('/', '-')
			assert os.path.exists(filename), 'ERROR: file %r of type %r does not exist' % (filename, option_type)
			hash_buffer = hashlib.sha1(buffers[src_fn]).hexdigest()
			hash_file = hashlib.sha1(open(filename).read()).hexdigest()
			if hash_buffer != hash_file:
				print('\n'.join(difflib.context_diff(open(filename).read(), buffers[src_fn], fromfile='filename', tofile='buffer')))
				pytest.fail('ERROR: sha1 sums of file and buffer differ (fn=%s ; file=%s ; buffer=%s)' % (filename, hash_file, hash_buffer))

		call_unjoin_script('66%s-uninstall.uinst' % package_name)

		# wait until removed object has been handled by the listener
		wait_for_replication()

		dnlist = get_dn_of_extension_by_name(extension_type, extension_name)
		assert not dnlist, 'ERROR: UDM extension object with cn=%s is still present in LDAP' % extension_name

		# check if registered file has been removed from local system
		assert not os.path.exists(target_fn), 'ERROR: target file %s is still present' % target_fn
		print('FILE HAS BEEN REMOVED: %r' % target_fn)
