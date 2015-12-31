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

from euca2ools.commands.elasticloadbalancing import ELBRequest
from euca2ools.commands.elasticloadbalancing.argtypes import listener
from requestbuilder import Arg


class CreateLoadBalancerListeners(ELBRequest):
    DESCRIPTION = 'Add one or more listeners to a load balancer'
    ARGS = [Arg('LoadBalancerName', metavar='ELB',
                help='name of the load balancer to modify (required)'),
            Arg('-l', '--listener', dest='Listeners.member', action='append',
                metavar=('"lb-port=PORT, protocol={HTTP,HTTPS,SSL,TCP}, '
                         'instance-port=PORT, instance-protocol={HTTP,HTTPS,'
                         'SSL,TCP}, cert-id=ARN"'), required=True,
                type=listener,
                help='''port/protocol settings for the load balancer, where
                lb-port is the external port number, protocol is the external
                protocol, instance-port is the back end server port number,
                instance-protocol is the protocol to use for routing traffic to
                back end instances, and cert-id is the ARN of the server
                certificate to use for encrypted connections.  lb-port,
                protocol, and instance-port are required.  This option may be
                used multiple times.  (at least 1 required)''')]
