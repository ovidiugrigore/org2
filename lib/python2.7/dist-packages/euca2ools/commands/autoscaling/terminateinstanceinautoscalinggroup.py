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

import argparse

from requestbuilder import Arg, MutuallyExclusiveArgList
from requestbuilder.mixins import TabifyingMixin

from euca2ools.commands.autoscaling import AutoScalingRequest


class TerminateInstanceInAutoScalingGroup(AutoScalingRequest,
                                          TabifyingMixin):
    DESCRIPTION = "Manually terminate an auto-scaling instance"
    ARGS = [Arg('InstanceId', metavar='INSTANCE',
                help='ID of the instance to terminate (required)'),
            MutuallyExclusiveArgList(
                Arg('-d', '--decrement-desired-capacity', action='store_const',
                    dest='ShouldDecrementDesiredCapacity', const='true',
                    help='''also reduce the desired capacity of the
                    auto-scaling group by 1'''),
                Arg('-D', '--no-decrement-desired-capacity',
                    dest='ShouldDecrementDesiredCapacity',
                    action='store_const', const='false',
                    help='''leave the auto-scaling group's desired capacity
                    as-is.  A new instance may be launched to compensate for
                    the one being terminated.'''))
            .required(),
            Arg('--show-long', action='store_true', route_to=None,
                help='show extra info about the instance being terminated'),
            Arg('-f', '--force', action='store_true', route_to=None,
                help=argparse.SUPPRESS)]  # for compatibility

    def print_result(self, result):
        activity = result['Activity']
        bits = ['INSTANCE',
                activity.get('ActivityId'),
                activity.get('EndTime'),
                activity.get('StatusCode'),
                activity.get('Cause')]
        if self.args['show_long']:
            bits.append(activity.get('StatusMessage'))
            bits.append(activity.get('Progress'))
            bits.append(activity.get('Description'))
            bits.append(activity.get('StartTime'))
        print self.tabify(bits)
