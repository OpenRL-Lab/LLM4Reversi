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

from reversi_tool.agents.base_agent import BaseAgent
from reversi_tool.agents.random_agent import RandomAgent
from reversi_tool.agents.llm_agent import LLMAgent


class QQGameAgent(BaseAgent):
    def __init__(self):
        self.agent = self.init_agent()

    def init_agent(self):
        return LLMAgent(name="QQGameAgent")

    def web_act(self, board, nexts, side=None):
        # 黑棋先走，黑棋是action2(即agent2)，黑子在棋盘上表示为1，side=1时，表示下黑棋。side=-1时，表示下白棋
        assert side in [1, -1], "side must be 1 or -1"
        return self.agent.web_act(board, nexts, side)
