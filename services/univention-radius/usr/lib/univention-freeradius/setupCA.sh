#!/bin/bash
#
# Copyright (C) 2011-2022 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of the software contained in this package
# as well as the source package itself are made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this package provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use the software under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

sslbase="/etc/freeradius/ssl"

if [ -d "$sslbase/ucsCA" ] ; then
	echo "Creation of new SSL-CA for freeradius has been skipped - already present"
	exit 0
fi

# shellcheck source=/dev/null
. /usr/share/univention-ssl/make-certificates.sh

TMPDIR="$(mktemp -d -t setupCA.XXXXXXXXXX)"
# shellcheck disable=SC2064
trap "rm -rf '$TMPDIR'" 0               # EXIT
# shellcheck disable=SC2064
trap "rm -rf '$TMPDIR'; exit 1" 2       # INT
# shellcheck disable=SC2064
trap "rm -rf '$TMPDIR'; exit 1" 1 15    # HUP TERM

[ ! -e "$sslbase/dh" ] && openssl dhparam -out "$TMPDIR/dh" 1024 && chmod 444 "$TMPDIR/dh"

init

mv "$TMPDIR/dh" "$sslbase"

name="univention-freeradius"
gencert "$sslbase/$name" "$name"
chmod -R g+rx "$sslbase/$name"
