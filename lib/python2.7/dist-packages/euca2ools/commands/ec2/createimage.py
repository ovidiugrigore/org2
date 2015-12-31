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

from requestbuilder import Arg

from euca2ools.commands.argtypes import ec2_block_device_mapping
from euca2ools.commands.ec2 import EC2Request


class CreateImage(EC2Request):
    DESCRIPTION = 'Create an EBS image from a running or stopped EBS instance'
    ARGS = [Arg('InstanceId', metavar='INSTANCE',
                help='instance from which to create the image (required)'),
            Arg('-n', '--name', dest='Name', required=True,
                help='name for the new image (required)'),
            Arg('-d', '--description', dest='Description', metavar='DESC',
                help='description for the new image'),
            Arg('--no-reboot', dest='NoReboot', action='store_const',
                const='true', help='''do not shut down the instance before
                creating the image. Image integrity may be affected.'''),
            Arg('-b', '--block-device-mapping', metavar='DEVICE=MAPPED',
                dest='BlockDeviceMapping', action='append',
                type=ec2_block_device_mapping, default=[],
                help='''define a block device mapping for the image, in the
                form DEVICE=MAPPED, where "MAPPED" is "none", "ephemeral(0-3)",
                or
                "[SNAP_ID]:[GiB]:[true|false]:[standard|VOLTYPE[:IOPS]]"''')]

    def print_result(self, result):
        print self.tabify(('IMAGE', result.get('imageId')))
