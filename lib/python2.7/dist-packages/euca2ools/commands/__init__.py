# Copyright 2009-2014 Eucalyptus Systems, Inc.
#
# Redistribution and use of this software in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import glob
import os.path
import platform
import sys

import requestbuilder
import requests

from euca2ools import __version__


DATADIR = '/usr/share/euca2ools'
SYSCONFDIR = '/etc/euca2ools'
USERCONFDIR = '~/.euca'


class Euca2ools(object):
    """
    A class with attributes and methods that define the entire euca2ools suite
    """

    CONFIG_PATHS = (os.path.join(SYSCONFDIR, 'euca2ools.ini'),
                    os.path.join(SYSCONFDIR, 'conf.d', '*.ini'),
                    os.path.join(USERCONFDIR, '*.ini'))

    def __init__(self):
        self.__user_agent = None

    # noinspection PyBroadException
    @staticmethod
    def format_version():
        version_lines = ['euca2ools {0} (Omega)'.format(__version__)]
        try:
            if os.path.isfile('/etc/eucalyptus/eucalyptus-version'):
                with open('/etc/eucalyptus/eucalyptus-version') as ver_file:
                    euca_version = ver_file.readline().strip()
                version_lines.append('eucalyptus {0}'.format(euca_version))
        except:
            # Those were just more crunchy bits.  If they don't work, oh well!
            pass
        return '\n'.join(version_lines)

    def list_config_files(self):
        config_files = []
        if 'EUCA_CONFIG_PATH' in os.environ:
            config_globs = os.getenv('EUCA_CONFIG_PATH').split(':')
        else:
            config_globs = self.CONFIG_PATHS
        for config_glob in config_globs:
            expanded = os.path.expanduser(os.path.expandvars(config_glob))
            config_files.extend(sorted(glob.glob(expanded)))
        return config_files

    def get_user_agent(self):
        if self.__user_agent is None:
            user_agent_bits = ['euca2ools/{0}'.format(__version__)]

            tokens = []
            impl = platform.python_implementation()
            if impl == 'PyPy':
                # pylint: disable=E1101
                impl_version = '{0}.{1}.{2}'.format(
                    sys.pypy_version_info.major,
                    sys.pypy_version_info.minor,
                    sys.pypy_version_info.micro)
                if sys.pypy_version_info.releaselevel != 'final':
                    impl_version += sys.pypy_version_info.releaselevel
                # pylint: enable=E1101
            else:
                # I'm guessing for non-CPython implementations; feel free to
                # submit patches or the needed implementation-specific API
                # references.
                impl_version = platform.python_version()
            tokens.append('{0} {1}'.format(impl, impl_version))
            plat = []
            try:
                plat.append(platform.system())
                plat.append(platform.release())
            except IOError:
                pass
            if plat:
                tokens.append(' '.join(plat))
            tokens.append(platform.machine())
            user_agent_bits.append('({0})'.format('; '.join(tokens)))

            user_agent_bits.append('requestbuilder/{0}'.format(
                requestbuilder.__version__))
            user_agent_bits.append('requests/{0}'.format(requests.__version__))
            self.__user_agent = ' '.join(user_agent_bits)
        return self.__user_agent
