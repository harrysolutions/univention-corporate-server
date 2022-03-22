#!/usr/share/ucs-test/runner pytest-3 -s -vvv
## desc: check if service specific password works as expected
## tags: [apptest, radius]
## packages:
##   - univention-radius
## join: true
## exposure: dangerous

import pytest
import subprocess
import univention.admin


def radius_auth(username, password):
	subprocess.check_call([
		'radtest',
		'-t',
		'mschap',
		username,
		password,
		'127.0.0.1:18120',
		'0',
		'testing123',
	])


@pytest.fixture
def credentials(user_type, rad_user, ucr):
	if user_type == 'user':
		return (rad_user[0], rad_user[2])
	elif user_type == 'computer':
		return (ucr.get('ldap/hostdn'), open('/etc/machine.secret').read())
	elif user_type == 'admin':
		return (ucr.get('tests/domainadmin/account'), ucr.get('tests/domainadmin/pwd'))
	assert False


@pytest.mark.parametrize('allowed,user_type', [
	(False, 'user'),
	(True, 'computer'),
	(True, 'admin'),
])
def test_acl_read_access(rad_user, lo, ssp, allowed, credentials):
	dn, name, password = rad_user
	binddn, bindpw = credentials
	lo.modify(dn, [('univentionRadiusPassword', [b'old'], [ssp[1]])])
	output = subprocess.check_output(['univention-ldapsearch', '-D', binddn, '-w', bindpw, '-b', dn, 'univentionRadiusPassword'])
	output = output.decode('utf-8')
	if allowed:
		assert 'univentionRadiusPassword:' in output
	else:
		assert 'univentionRadiusPassword:' not in output


@pytest.mark.parametrize('allowed,user_type', [
	(False, 'user'),
	(False, 'computer'),
	(True, 'admin'),
])
def test_acl_write_access(rad_user, ssp, ucr, allowed, credentials):
	dn, name, password = rad_user
	binddn, bindpw = credentials
	lo = univention.admin.uldap.access(host=ucr.get('ldap/master'), port=ucr.get('ldap/server/port'), base=ucr.get('ldap/base'), binddn=binddn, bindpw=bindpw, start_tls=2, follow_referral=True)
	if allowed:
		lo.modify(dn, (('univentionRadiusPassword', [b''], [ssp[1]]),))
	else:
		with pytest.raises(univention.admin.uexceptions.permissionDenied):
			lo.modify(dn, (('univentionRadiusPassword', [b''], [ssp[1]]),))
