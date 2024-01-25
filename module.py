#!/usr/bin/python3
# coding=utf-8

#   Copyright 2024 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Module """

from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import module  # pylint: disable=E0611,E0401

from arbiter import RedisEventNode  # pylint: disable=E0611,E0401


class Module(module.ModuleModel):
    """ Pylon module """

    def __init__(self, context, descriptor):
        self.context = context
        self.descriptor = descriptor
        #
        self.event_node = RedisEventNode(**self.descriptor.config.get("event_node"))
        self.room_cache = {}

    def init(self):
        """ Init module """
        log.info("Initializing module")
        # Init
        self.descriptor.init_all()
        # EventNode
        self.event_node.start()
        self.event_node.subscribe("log_data", self.on_log_data)

    def deinit(self):
        """ De-init module """
        log.info("De-initializing module")
        # EventNode
        self.event_node.unsubscribe("log_data", self.on_log_data)
        self.event_node.stop()
        # De-init
        # self.descriptor.deinit_all()
