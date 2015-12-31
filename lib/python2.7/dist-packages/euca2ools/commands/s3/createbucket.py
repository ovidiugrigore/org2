# Copyright 2013-2014 Eucalyptus Systems, Inc.
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

import xml.etree.ElementTree as ET

from requestbuilder import Arg

from euca2ools.commands.s3 import S3Request, validate_generic_bucket_name


class CreateBucket(S3Request):
    DESCRIPTION = 'Create a new bucket'
    ARGS = [Arg('bucket', route_to=None, help='name of the new bucket'),
            Arg('--location', route_to=None,
                help='''location constraint to configure the bucket with
                (default: inferred from s3-location-constraint in
                configuration, or otherwise none)''')]

    def configure(self):
        S3Request.configure(self)
        validate_generic_bucket_name(self.args['bucket'])

    def preprocess(self):
        self.method = 'PUT'
        self.path = self.args['bucket']
        cb_config = ET.Element('CreateBucketConfiguration')
        cb_config.set('xmlns', 'http://doc.s3.amazonaws.com/2006-03-01')
        lconstraint = (self.args.get('location') or
                       self.config.get_region_option('s3-location-constraint'))
        if lconstraint:
            cb_lconstraint = ET.SubElement(cb_config, 'LocationConstraint')
            cb_lconstraint.text = lconstraint
        if len(cb_config.getchildren()):
            cb_xml = ET.tostring(cb_config)
            self.log.debug('bucket configuration: %s', cb_xml)
            self.body = cb_xml
