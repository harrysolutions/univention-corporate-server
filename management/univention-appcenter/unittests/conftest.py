#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2022 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.
#


import sys
from glob import glob
import logging

from univentionunittests import import_module
from univentionunittests.umc import import_umc_module, save_result_on_request


import pytest


@pytest.fixture
def mocked_connection(mocker, lo, pos):
	udm_module = _import('udm')
	mocker.patch.object(udm_module, 'getMachineConnection', return_value=[lo, pos])
	mocker.patch.object(udm_module, 'getAdminConnection', return_value=[lo, pos])
	return lo


@pytest.fixture
def get_action():
	actions_module = _import('actions')
	return actions_module.get_action


@pytest.fixture
def mocked_ucr_appcenter(mocked_ucr, mocker):
	ucr_module = _import('ucr')
	mocker.patch.object(ucr_module, '_UCR', mocked_ucr)

	def ucr_save(values):
		changed_values = {}
		for k, v in values.items():
			if mocked_ucr.get(k) != v:
				changed_values[k] = v
		if changed_values:
			mocked_ucr.items.update(changed_values)
		return changed_values
	mocker.patch.object(ucr_module, 'ucr_save', ucr_save)

	mocked_ucr['uuid/license'] = '00000000-0000-0000-0000-000000000000'
	mocked_ucr['server/role'] = 'domaincontroller_master'
	mocked_ucr['hostname'] = 'master'
	mocked_ucr['domainname'] = 'intranet.example.de'
	mocked_ucr['version/version'] = '5.0'
	mocked_ucr['version/patchlevel'] = '0'
	mocked_ucr['version/erratalevel'] = '0'
	mocked_ucr['repository/app_center/server'] = 'https://appcenter.software-univention.de'
	return mocked_ucr


@pytest.fixture
def custom_apps(mocker):
	cache_module = _import('app_cache')
	app_module = _import('app')
	Apps = cache_module.Apps

	def get_every_single_app(self):
		return self._test_apps

	def load(self, path):
		for ini in glob(path + '/*/*.ini'):
			app = app_module.App.from_ini(ini)
			self._test_apps.append(app)
	mocker.patch.object(Apps, 'get_every_single_app', get_every_single_app)
	Apps.load = load
	Apps._test_apps = []
	yield Apps()
	del Apps._test_apps
	del Apps.load


def pytest_addoption(parser):
	parser.addoption("--installed-appcenter", action="store_true", help="Test against installed appcenter installation (not src)")


def import_appcenter_modules():
	use_installed = pytest.config.getoption('--installed-appcenter')
	local_python_path = 'python/appcenter/'
	# for pymod in glob(local_python_path + '*.py'):
	# 	name = os.path.basename(pymod)[:-3]
	import_module('listener', None, 'listener', use_installed=True)
	for name in ['log', 'ucr', 'utils', 'packages', 'meta', 'ini_parser', 'settings', 'app', 'app_cache', 'udm', 'actions', 'install_checks']:
		module = import_module(name, local_python_path, 'univention.appcenter.{}'.format(name), use_installed=use_installed)
		if name == 'log':
			module.log_to_stream()
			logger = module.get_base_logger()
			for handler in logger.handlers:
				for filter in handler.filters:
					if hasattr(filter, 'min_level'):
						filter.min_level = logging.DEBUG
		if name == 'actions':
			if not use_installed:
				import os.path
				for pymodule in glob('python/appcenter/actions/*.py'):
					name = os.path.basename(pymodule)[:-3]  # without .py
					local_python_path = os.path.dirname(pymodule)
					import_module(name, local_python_path, 'univention.appcenter.actions.{}'.format(name), use_installed=use_installed)
				for pymodule in glob('python/appcenter-docker/actions/service.py'):
					name = os.path.basename(pymodule)[:-3]  # without .py
					local_python_path = os.path.dirname(pymodule)
					import_module(name, local_python_path, 'univention.appcenter.actions.{}'.format(name), use_installed=use_installed)
				for pymodule in glob('python/appcenter-docker/actions/docker_base.py'):
					name = os.path.basename(pymodule)[:-3]  # without .py
					local_python_path = os.path.dirname(pymodule)
					import_module(name, local_python_path, 'univention.appcenter.actions.{}'.format(name), use_installed=use_installed)
				for pymodule in glob('python/appcenter-docker/actions/docker_*.py'):
					name = os.path.basename(pymodule)[:-3]  # without .py
					local_python_path = os.path.dirname(pymodule)
					import_module(name, local_python_path, 'univention.appcenter.actions.{}'.format(name), use_installed=use_installed)
				for pymodule in glob('python/appcenter-docker/actions/*.py'):
					name = os.path.basename(pymodule)[:-3]  # without .py
					local_python_path = os.path.dirname(pymodule)
					import_module(name, local_python_path, 'univention.appcenter.actions.{}'.format(name), use_installed=use_installed)


def _import(name):
	import_appcenter_modules()
	return sys.modules['univention.appcenter.{}'.format(name)]


@pytest.fixture
def imported_appcenter_modules():
	import_appcenter_modules()


@pytest.fixture
def import_appcenter_module():
	return _import


@pytest.fixture
def appcenter_umc_instance(imported_appcenter_modules, mocker):
	appcenter = import_umc_module('appcenter')
	mocker.patch.object(appcenter.Instance, 'finished', side_effect=save_result_on_request)
	instance = appcenter.Instance()
	instance.init()
	return instance
