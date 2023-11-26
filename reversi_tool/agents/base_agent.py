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


class BaseAgent:
    def __init__(self, name="BaseAgent", side=None):
        # side为1的话，则为黑方，side为-1的话，则为白方
        self.name = name
        self.side = side

    def set_side(self, side):
        # side为1的话，则为黑方，side为-1的话，则为白方
        self.side = side

    def web_act(self, board, nexts, side=None):
        # 黑棋先走，黑子在棋盘上表示为1, side为1的话，则为黑方，side为-1的话，则为白方
        pass
