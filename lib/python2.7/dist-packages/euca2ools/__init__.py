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

import os.path
import subprocess


__version__ = '3.1.0'

BUFSIZE = 8192


if '__file__' in globals():
    # Check if this is a git repo; maybe we can get more precise version info
    try:
        REPO_PATH = os.path.join(os.path.dirname(__file__), '..')
        # noinspection PyUnresolvedReferences
        GIT = subprocess.Popen(
            ['git', 'describe'], stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={'GIT_DIR': os.path.join(REPO_PATH, '.git')})
        GIT.wait()
        GIT.stderr.read()
        if GIT.returncode == 0:
            __version__ = GIT.stdout.read().strip().lstrip('v')
            if type(__version__).__name__ == 'bytes':
                __version__ = __version__.decode()
    except:
        # Not really a bad thing; we'll just use what we had
        pass
