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

from euca2ools.commands.ec2 import EC2Request
from requestbuilder import Arg


class CopyImage(EC2Request):
    DESCRIPTION = ('Copy an image from another region\n\nRun this command '
                   'against the destination region, not the source region.')
    ARGS = [Arg('-r', '--source-region', dest='SourceRegion', metavar='REGION',
                required=True,
                help='name of the region to copy the image from (required)'),
            Arg('-s', '--source-ami-id', dest='SourceImageId', metavar='IMAGE',
                required=True,
                help='ID of the image to copy (required)'),
            Arg('-n', '--name', dest='Name',
                help='name to assign the new copy of the image'),
            Arg('-d', '--description', dest='Description', metavar='DESC',
                help='description to assign the new copy of the image'),
            Arg('-c', '--client-token', dest='ClientToken', metavar='TOKEN',
                help='unique identifier to ensure request idempotency')]

    def print_result(self, result):
        print self.tabify(('IMAGE', result.get('imageId')))
