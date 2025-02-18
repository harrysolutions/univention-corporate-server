# -*- coding: utf-8 -*-
#
# Copyright 2017-2022 Univention GmbH
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
# you and Univention.
#
# This program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

"""
Get a Python logging object below a listener module root logger.
The new logging object can log to a stream or a file.
The listener module root logger will log messages of all of its children
additionally to the common `listener.log`.
"""

#
# Code mostly copied and adapted from
# ucs-school-4.2/ucs-school-lib/python/models/utils.py
#

from __future__ import absolute_import

import grp
import logging
import os
import pwd
import stat
import syslog
from collections import Mapping
from logging.handlers import TimedRotatingFileHandler
from six import string_types, text_type, PY2
from typing import Any, Dict, IO, Optional, Type  # noqa F401

import listener
import univention.debug as ud
from univention.config_registry import ConfigRegistry


__syslog_opened = False


class UniFileHandler(TimedRotatingFileHandler):
	"""
	Used by listener modules using the :py:mod:`univention.listener` API to
	write log files below :file:`/var/log/univention/listener_log/`.
	Configuration can be done through the `handler_kwargs` argument of
	:py:func:`get_listener_logger`.
	"""
	def _open(self):
		# type: () -> IO[str]
		stream = TimedRotatingFileHandler._open(self)
		file_stat = os.fstat(stream.fileno())
		listener_uid = pwd.getpwnam('listener').pw_uid
		adm_gid = grp.getgrnam('adm').gr_gid
		if file_stat.st_uid != listener_uid or file_stat.st_gid != adm_gid:
			old_uid = os.geteuid()
			try:
				if old_uid != 0:
					listener.setuid(0)
				os.fchown(stream.fileno(), listener_uid, adm_gid)
				os.fchmod(stream.fileno(), stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP)
			finally:
				if old_uid != 0:
					listener.unsetuid()
		return stream


class ModuleHandler(logging.Handler):
	"""
	Used by listener modules using the :py:mod:`univention.listener` API to
	write log messages through :py:mod:`univention.debug` to
	:file:`/var/log/univention/listener.log`
	"""
	LOGGING_TO_UDEBUG = dict(
		CRITICAL=ud.ERROR,
		ERROR=ud.ERROR,
		WARN=ud.WARN,
		WARNING=ud.WARN,
		INFO=ud.PROCESS,
		DEBUG=ud.INFO,
		NOTSET=ud.INFO
	)

	def __init__(self, level=logging.NOTSET, udebug_facility=ud.LISTENER):
		# type: (int, int) -> None
		self._udebug_facility = udebug_facility
		super(ModuleHandler, self).__init__(level)

	def emit(self, record):
		# type: (logging.LogRecord) -> None
		msg = self.format(record)
		if PY2 and isinstance(msg, text_type):
			msg = msg.encode('utf-8')
		msg = '{}: {}'.format(record.name.rsplit('.')[-1], msg)
		udebug_level = self.LOGGING_TO_UDEBUG[record.levelname]
		ud.debug(self._udebug_facility, udebug_level, msg)


__LF_D = '%(asctime)s %(levelname)-7s %(module)s.%(funcName)s:%(lineno)d  %(message)s'
__LF_I = '%(asctime)s %(levelname)-7s %(message)s'
FILE_LOG_FORMATS = dict(
	NOTSET=__LF_D,
	DEBUG=__LF_D,
	INFO=__LF_I,
	WARNING=__LF_I,
	WARN=__LF_I,
	ERROR=__LF_I,
	CRITICAL=__LF_I,
)

__LC_D = '%(asctime)s %(levelname)-7s %(module)s.%(funcName)s:%(lineno)d  %(message)s'
__LC_I = '%(message)s'
__LC_W = '%(levelname)-7s  %(message)s'
CMDLINE_LOG_FORMATS = dict(
	NOTSET=__LC_D,
	DEBUG=__LC_D,
	INFO=__LC_I,
	WARNING=__LC_W,
	WARN=__LC_W,
	ERROR=__LC_W,
	CRITICAL=__LC_W,
)

UCR_DEBUG_LEVEL_TO_LOGGING_LEVEL = {
	0: 'ERROR',
	1: 'WARN',
	2: 'INFO',
	3: 'DEBUG',
	4: 'DEBUG',
}

LOG_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

_logger_cache = {}  # type: Dict[str, logging.Logger]
_handler_cache = {}  # type: Dict[str, UniFileHandler]
_ucr = ConfigRegistry()
_ucr.load()


def _get_ucr_int(ucr_key, default):
	# type: (str, int) -> int
	try:
		return int(_ucr.get(ucr_key, default))
	except ValueError:
		return default


_listener_debug_level = _get_ucr_int('listener/debug/level', 2)
_listener_debug_level_str = UCR_DEBUG_LEVEL_TO_LOGGING_LEVEL[max(0, min(4, _listener_debug_level))]
_listener_module_handler = ModuleHandler(level=getattr(logging, _listener_debug_level_str))
listener_module_root_logger = logging.getLogger('listener module')
listener_module_root_logger.setLevel(getattr(logging, _listener_debug_level_str))


def get_logger(name, path=None):
	# type: (str, Optional[str]) -> logging.Logger
	"""
	Get a logging instance. Caching wrapper for
	:py:func:`get_listener_logger()`.

	:param str name: name of the logger instance will be `<root loggers name>.name`
	:param str path: path to log file to create. If unset will be
		`/var/log/univention/listener_modules/<name>.log`.
	:return: a Python logging object
	:rtype: logging.Logger
	"""
	if name not in _logger_cache:
		file_name = name.replace('/', '_')
		logger_name = name.replace('.', '_')
		log_dir = '/var/log/univention/listener_modules'
		file_path = path or os.path.join(log_dir, '{}.log'.format(file_name))
		listener_uid = pwd.getpwnam('listener').pw_uid
		adm_grp = grp.getgrnam('adm').gr_gid
		if not os.path.isdir(log_dir):
			old_uid = os.geteuid()
			try:
				if old_uid != 0:
					listener.setuid(0)
				os.mkdir(log_dir)
				os.chown(log_dir, listener_uid, adm_grp)
				os.chmod(
					log_dir,
					stat.S_ISGID | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP
				)
			finally:
				if old_uid != 0:
					listener.unsetuid()
		_logger_cache[name] = get_listener_logger(logger_name, file_path)
	return _logger_cache[name]


def calculate_loglevel(name):
	# type: (str) -> str
	"""
	Returns the higher of `listener/debug/level` and `listener/module/<name>/debug/level`
	which is the lower log level.

	:param str name: name of logger instance
	:return: log level
	:rtype: int
	"""
	listener_module_debug_level = _get_ucr_int('listener/module/{}/debug/level'.format(name), 2)
	# 0 <= ucr level <= 4
	return UCR_DEBUG_LEVEL_TO_LOGGING_LEVEL[min(4, max(0, _listener_debug_level, listener_module_debug_level))]


def get_listener_logger(name, filename, level=None, handler_kwargs=None, formatter_kwargs=None):
	# type: (str, str, Optional[str], Optional[Dict[str, Any]], Optional[Dict[str, Any]]) -> logging.Logger
	"""
	Get a logger object below the listener module root logger. The logger
	will additionally log to the common `listener.log`.

	* The logger will use UniFileHandler(TimedRotatingFileHandler) for files if
	  not configured differently through `handler_kwargs[cls]`.
	* A call with the same name will return the same logging object.
	* There is only one handler per name-target combination.
	* If name and target are the same, and only the log level changes, it will
	  return the logging object with the same handlers and change both the log
	  level of the respective handler and of the logger object to be the lowest
	  of the previous and the new level.
	* The loglevel will be the lowest one of `INFO` and the UCRVs
	  `listener/debug/level` and `listener/module/<name>/debug/level`.
	* Complete output customization is possible, setting kwargs for the
	  constructors of the handler and formatter.
	* Using custom handler and formatter classes is possible by configuring
	  the `cls` key of `handler_kwargs` and `formatter_kwargs`.

	:param str name: name of the logger instance will be `<root loggers name>.name`
	:param str level: loglevel (`DEBUG`, `INFO` etc) or if not set it will be chosen
		automatically (see above)
	:param str target: (file path)
	:param dict handler_kwargs: will be passed to the handlers constructor.
		It cannot be used to modify a handler, as it is only used at creation time.
		If it has a key `cls` it will be used as handler instead of :py:class:`UniFileHandler`
		or :py:class:`UniStreamHandler`. It should be a subclass of one of those!
	:param dict formatter_kwargs: will be passed to the formatters constructor,
		if it has a key `cls` it will be used to create a formatter instead of
		:py:class`logging.Formatter`.
	:return: a Python logging object
	:rtype: logging.Logger
	"""  # noqa: E101
	assert isinstance(filename, string_types)
	assert isinstance(name, string_types)
	if not name:
		name = 'noname'
	name = name.replace('.', '_')  # don't mess up logger hierarchy
	cache_key = '{}-{}'.format(name, filename)
	logger_name = '{}.{}'.format(listener_module_root_logger.name, name)
	_logger = logging.getLogger(logger_name)

	if not level:
		level = calculate_loglevel(name)

	if cache_key in _handler_cache and getattr(logging, level) >= _handler_cache[cache_key].level:
		return _logger

	if not isinstance(handler_kwargs, Mapping):
		handler_kwargs = {}
	if not isinstance(formatter_kwargs, Mapping):
		formatter_kwargs = {}

	# The logger objects level must be the lowest of all handlers, or handlers
	# with a higher level will not be able to log anything.
	if getattr(logging, level) < _logger.level:
		_logger.setLevel(level)

	if _logger.level == logging.NOTSET:
		# fresh logger
		_logger.setLevel(level)

	fmt = FILE_LOG_FORMATS[level]
	fmt_kwargs = dict(cls=logging.Formatter, fmt=fmt, datefmt=LOG_DATETIME_FORMAT)  # type: Dict[str, Any]
	fmt_kwargs.update(formatter_kwargs)

	if cache_key in _handler_cache:
		# Check if loglevel from this request is lower than the one used in
		# the cached loggers handler. We do only lower level, never raise it.
		if getattr(logging, level) < _handler_cache[cache_key].level:
			handler = _handler_cache[cache_key]
			handler.setLevel(level)
			formatter_cls = fmt_kwargs.pop('cls')  # type: Type[logging.Formatter]
			formatter = formatter_cls(**fmt_kwargs)
			handler.setFormatter(formatter)
	else:
		# Create handler and formatter from scratch.
		handler = UniFileHandler(filename=filename, when='W6', backupCount=60, **handler_kwargs)
		handler.set_name(logger_name)
		handler.setLevel(level)
		formatter_cls = fmt_kwargs.pop('cls')
		formatter = formatter_cls(**fmt_kwargs)
		handler.setFormatter(formatter)
		_logger.addHandler(handler)
		_handler_cache[cache_key] = handler
	if _listener_module_handler not in listener_module_root_logger.handlers:
		listener_module_root_logger.addHandler(_listener_module_handler)
	return _logger


def _log_to_syslog(level, msg):
	# type: (int, str) -> None
	if not __syslog_opened:
		syslog.openlog('Listener', 0, syslog.LOG_SYSLOG)

	syslog.syslog(level, msg)


def info_to_syslog(msg):
	# type: (str) -> None
	_log_to_syslog(syslog.LOG_INFO, msg)
