#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2023 The OpenRL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""""""

from reversi_tool.agents.web_base import BaseWebAgent
from reversi_tool.agents.human import Human
from reversi_tool.agents.random_agent import RandomAgent
from reversi_tool.agents.llm_agent import LLMAgent


class BlackSideAgent(BaseWebAgent):
    def init_agent(self):
        # return RandomAgent(name="BlackSideAgent", side=1)
        return LLMAgent(player_type=1, name="BlackSideAgent")
