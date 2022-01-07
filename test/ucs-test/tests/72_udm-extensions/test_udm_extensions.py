#!/usr/share/ucs-test/runner pytest-3
# i will in a later commit merge the other files into this one
# for now i used it for shared functions / fixtures
from contextlib import contextmanager
from univention.testing.debian_package import DebianPackage
from univention.testing.udm_extensions import (
	remove_extension_by_name
)


@contextmanager
def temp_deb_pkg(package_name, package_version, extension_type, extension_name):
	package = DebianPackage(name=package_name, version=package_version)
	try:
		yield package
	finally:
		remove_extension_by_name(extension_type, extension_name, fail_on_error=False)
		package.uninstall()
		package.remove()
