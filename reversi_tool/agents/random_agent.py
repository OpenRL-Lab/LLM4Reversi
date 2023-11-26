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

import random

import numpy as np
from reversi_tool.agents.base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def web_act(self, board, nexts, side=None):
        # 黑棋先走，黑棋是action2(即agent2)，黑子在棋盘上表示为1
        print("name: ", self.name, " board: \n", np.array(board).reshape(8, 8), " nexts: ", nexts)
        if nexts == []:
            action = None
        else:
            action = random.sample(nexts, 1)[0]
        return action
