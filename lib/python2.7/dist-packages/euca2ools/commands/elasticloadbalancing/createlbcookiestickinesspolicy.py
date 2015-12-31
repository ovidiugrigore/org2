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
from requestbuilder import Arg


class CreateLBCookieStickinessPolicy(ELBRequest):
    DESCRIPTION = ('Create a new stickiness policy for a load balancer, '
                   'whereby the load balancer automatically generates cookies '
                   'that it uses to route requests from each user to the same '
                   'back end instance.  This type of policy can only be '
                   'associated with HTTP or HTTPS listeners.')
    ARGS = [Arg('LoadBalancerName', metavar='ELB',
                help='name of the load balancer to modify (required)'),
            Arg('-e', '--expiration-period', dest='CookieExpirationPeriod',
                metavar='SECONDS', type=int, required=True,
                help='''time period after which cookies should be considered
                stale (default: user's session length) (required)'''),
            Arg('-p', '--policy-name', dest='PolicyName', metavar='POLICY',
                required=True, help='name of the new policy (required)')]
