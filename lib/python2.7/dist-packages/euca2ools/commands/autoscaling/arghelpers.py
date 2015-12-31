# Copyright 2013 Eucalyptus Systems, Inc.
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

from euca2ools.commands.autoscaling.argtypes import autoscaling_tag_def
from requestbuilder import Arg


class TagArg(Arg):
    def __init__(self, required=False):
        helpstr = '''attributes of a tag to affect.  Tags follow the following
        format: "id=resource-name, t=resource-type, k=tag-key, v=tag-val,
        p=propagate-at-launch-flag", where k is the tag's name, v is the tag's
        value, id is a resource ID, t is a resource type, and p is whether to
        propagate tags to instances created by the group.  A value for 'k=' is
        required for each tag.  The rest are optional.  This argument may be
        used more than once.  Each time affects a different tag.'''

        if required:
            helpstr += '  (at least 1 required)'

        Arg.__init__(self, '--tag', dest='Tags.member', required=required,
                     action='append', type=autoscaling_tag_def, help=helpstr,
                     metavar=('"k=VALUE, id=VALUE, t=VALUE, v=VALUE, '
                              'p={true,false}"'))
