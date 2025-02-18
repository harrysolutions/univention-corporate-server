#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Univention Samba
#  this script creates samba configurations from ucr values
#
# Copyright 2004-2022 Univention GmbH
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

import sys

try:
	from univention.lib.share_restrictions import ShareConfiguration
except ImportError as exc:
	print('Could not import ShareConfiguration: %s' % (exc,), file=sys.stderr)
	sys.exit(0)

# main
if __name__ == '__main__':
	conf = ShareConfiguration()

	conf.read()

	# DEBUGGING
	# import pprint
	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint(conf.shares)
	# pp.pprint(conf.globals)
	# pp.pprint(conf.printers)
	# sys.exit(0)

	conf.write()
