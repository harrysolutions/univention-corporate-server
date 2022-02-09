#!/usr/bin/python3
import os
import sys
import json
import argparse
import tempfile
import univention.admin.modules

univention.admin.modules.update()


def pre():
	from univention.management.console.modules.udm.syntax import widget
	from univention.management.console.modules.udm.udm_ldap import read_syntax_choices, _module_cache
	options = {}
	choices = {}
	for name, module in univention.admin.modules.modules.items():
		_module_cache.get(name, ldap_connection=lo, ldap_position=po)
		for property_name, prop in module.property_descriptions.items():
			options.setdefault(name, {})[property_name] = widget(prop.syntax, prop.__dict__)
			try:
				choice = read_syntax_choices(prop.syntax, ldap_connection=lo, ldap_position=po)
			except KeyError as exc:
				choice = str(exc)  # dependencies
			choices.setdefault(name, {})[property_name] = choice
	return options, choices


def post():
	from univention.management.console.modules.udm.udm_ldap import read_syntax_choices, _module_cache
	options = {}
	choices = {}
	for name, module in univention.admin.modules.modules.items():
		_module_cache.get(name, ldap_connection=lo, ldap_position=po)
		for property_name, prop in module.property_descriptions.items():
			options.setdefault(name, {})[property_name] = prop.syntax.get_widget_options(prop)
			try:
				choice = read_syntax_choices(prop.syntax, ldap_connection=lo, ldap_position=po)
				#choice = prop.syntax.get_choices(lo, {})
			except KeyError as exc:
				choice = str(exc)  # dependencies
			choices.setdefault(name, {})[property_name] = choice
	return options, choices


def diff():
	diff = {}
	pre_contents = {}
	post_contents = {}
	with open('pre_options.json') as fd, open('post_options.json') as fd2, tempfile.NamedTemporaryFile(mode='w') as tmp, tempfile.NamedTemporaryFile(mode='w') as tmp2:
		pre, post = json.load(fd), json.load(fd2)
		assert pre.keys() == post.keys()
		for module in pre:
			old, new = pre[module], post[module]
			assert old.keys() == new.keys()
			for prop in old:
				#if prop in ('mailPrimaryAddress', 'mailDomain', 'mailAddress', 'allModuleOptions'):
				#	continue
				prop_pre, prop_post = old[prop], new[prop]

				if '$name$' in prop_pre.get('dynamicOptions', {}):
					prop_pre['dynamicOptions']['$depends$'] = prop_pre['dynamicOptions'].pop('$name$')

				if prop_pre.get('staticValues', []).count({'id': '', 'label': ''}) > 1:
					prop_pre['staticValues'].remove({'id': '', 'label': ''})

				from univention.management.console.modules.udm.udm_ldap import _module_cache
				_module_cache.get(module, ldap_connection=lo, ldap_position=po)
				try:
					syntax = univention.admin.modules.modules[module].property_descriptions[prop].syntax
				except KeyError:
					pass
				else:
					if syntax.name in ('emailAddressValidDomain', 'allModuleOptions', 'primaryEmailAddressValidDomain'):
						continue

				if prop_pre != prop_post:
					diff.setdefault(module, {}).setdefault(prop, syntax.name)
					#diff.setdefault(module, {}).setdefault(prop, [prop_pre, prop_post])
					print('\n\n\nModule: %s Property: %s Syntax: %s\n%s' % (module, prop, syntax.name, json.dumps(prop_pre, sort_keys=True, indent=4, separators=(',', ': '))), file=tmp)
					print('\n\n\nModule: %s Property: %s Syntax: %s\n%s' % (module, prop, syntax.name, json.dumps(prop_post, sort_keys=True, indent=4, separators=(',', ': '))), file=tmp2)

					pre_contents[syntax.name] = prop_pre
					post_contents[syntax.name] = prop_post
			print(json.dumps(diff, sort_keys=True, indent=4, separators=(',', ': ')))

			#json.dump(pre_contents, tmp, sort_keys=True, indent=4, separators=(',', ': '))
			#json.dump(post_contents, tmp2, sort_keys=True, indent=4, separators=(',', ': '))
			tmp.flush()
			tmp2.flush()

		os.execv('/usr/bin/vimdiff', ['vimdiff', tmp.name, tmp2.name])

#	os.execv('/bin/bash', ['bash', '-c', 'vimdiff <(python -m json.tool < pre_options.json) <(python -m json.tool < post_options.json)'])
#	os.execv('/bin/bash', ['bash', '-c', 'vimdiff <(python -m json.tool < pre_choices.json) <(python -m json.tool < post_choices.json)'])


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('case', choices=['pre', 'post', 'diff'])
	args = parser.parse_args()
	lo, po = univention.admin.uldap.getMachineConnection()

	if args.case == 'diff':
		diff()
		sys.exit(0)

	func = {'pre': pre, 'post': post}[args.case]
	options, choices = func()
	with open('%s_options.json' % (args.case,), 'w') as fd:
		json.dump(options, fd)
	with open('%s_choices.json' % (args.case,), 'w') as fd:
		json.dump(choices, fd)
