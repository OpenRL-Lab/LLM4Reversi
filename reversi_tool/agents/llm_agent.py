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

from typing import Optional

import numpy as np
import json
import re
import openai

from reversi_tool.agents.base_agent import BaseAgent

int2pos = {
    0: (1, 'A'), 1: (1, 'B'), 2: (1, 'C'), 3: (1, 'D'),
    4: (1, 'E'), 5: (1, 'F'), 6: (1, 'G'), 7: (1, 'H'),
    8: (2, 'A'), 9: (2, 'B'), 10: (2, 'C'), 11: (2, 'D'),
    12: (2, 'E'), 13: (2, 'F'), 14: (2, 'G'), 15: (2, 'H'),
    16: (3, 'A'), 17: (3, 'B'), 18: (3, 'C'), 19: (3, 'D'),
    20: (3, 'E'), 21: (3, 'F'), 22: (3, 'G'), 23: (3, 'H'),
    24: (4, 'A'), 25: (4, 'B'), 26: (4, 'C'), 27: (4, 'D'),
    28: (4, 'E'), 29: (4, 'F'), 30: (4, 'G'), 31: (4, 'H'),
    32: (5, 'A'), 33: (5, 'B'), 34: (5, 'C'), 35: (5, 'D'),
    36: (5, 'E'), 37: (5, 'F'), 38: (5, 'G'), 39: (5, 'H'),
    40: (6, 'A'), 41: (6, 'B'), 42: (6, 'C'), 43: (6, 'D'),
    44: (6, 'E'), 45: (6, 'F'), 46: (6, 'G'), 47: (6, 'H'),
    48: (7, 'A'), 49: (7, 'B'), 50: (7, 'C'), 51: (7, 'D'),
    52: (7, 'E'), 53: (7, 'F'), 54: (7, 'G'), 55: (7, 'H'),
    56: (8, 'A'), 57: (8, 'B'), 58: (8, 'C'), 59: (8, 'D'),
    60: (8, 'E'), 61: (8, 'F'), 62: (8, 'G'), 63: (8, 'H')
}


class LLMAgent(BaseAgent):
    def __init__(self, player_type: int = 1, name=None, config_path="../reversi_tool/agents/config/gpt4.json"):
        super().__init__(name=name)
        self.player_type = player_type
        self.config = json.load(open(config_path, 'r'))
        print("模型配置：", self.config)
        self.model_name = self.config.get("model", None)
        self.temperature = int(self.config.get("temperature", None))
        self.prompt_init = self.config.get("prompt_init", None)
        self.api_base = self.config.get("api_base", None)
        self.api_key = self.config.get("api_key", None)
        if self.api_base is None or self.api_base == "":
            print("请在reversi_tool/agents/config/gpt4.json文件中设置你的openai api url!")
            exit()
        if self.api_key is None or self.api_key == "":
            print("请在reversi_tool/agents/config/gpt4.json文件中设置你的openai api key!")
            exit()

        self.log_prompt = False
        self.log_board = False

    def get_chat_action(self, message):
        if self.api_base:
            openai.api_base = self.api_base
        openai.api_key = self.api_key

        self.messages = [{"role": "system", "content": self.prompt_init}, {"role": "user", "content": message}]

        try:
            answer = openai.ChatCompletion.create(
                model=self.model_name,
                messages=self.messages,
                temperature=self.temperature,
                timeout=15,
            )
        except:
            print("模型调用失败！")
            return None

        answer = answer['choices'][0]['message']['content']

        return answer

    def get_board_status_str(self, board):
        board_format = ""
        for i in range(8):
            # board_format += str(i + 1) + " "
            for j in range(8):
                piece = board[i * 8 + j]
                position = int2pos[i * 8 + j]
                position = "(" + f"{position[0]}{position[1]}" + ")"
                if piece == 1:
                    board_format += "B"
                elif piece == -1:
                    board_format += "W"
                else:
                    board_format += "-"
                board_format += position + " "
            board_format += "\n"
        return board_format
        # board = np.array(board).reshape(8, 8)
        # board_status_str = "\n"
        # board_status = [ [ j for j in range(i * 8,(i + 1) * 8)] for i in range(8) ]
        # for i in range(8):
        #     for j in range(8):
        #         if board[i][j] == 1:
        #             board_status[i][j] = "X"
        #         elif board[i][j] == -1:
        #             board_status[i][j] = "O"
        # for row in board_status:
        #     for col in row:
        #         if isinstance(col,int):
        #             board_status_str = board_status_str + f"| {col:2d} "
        #         else:
        #             board_status_str = board_status_str + f"|  {col} "
        #     board_status_str += "|\n"
        #
        # return board_status_str

    def get_next_str(self, nexts):
        return "[" + ', '.join(list(map(lambda x: str(x) + "(" + f"{int2pos[x][0]}{int2pos[x][1]}" + ")", nexts))) + "]"

    def retry(self, message, wrong_answer, color):
        retry_message = f"\n(Warning: Previously, your answer is: \"{wrong_answer}\",  which is not valid!)\n"
        retry_message = message + retry_message
        if self.log_prompt:
            print(retry_message)
        answer = self.get_chat_action(retry_message)
        if answer is None:
            return None
        if self.log_prompt:
            print("Retry answer:", answer)
        action = re.findall(rf'{color}:\s*([0-5][0-9]|6[0-3]|[0-9])', answer)
        if len(action) == 0:
            return None
        action = action[0]
        action = int(action)
        return action

    def act(self, board, nexts, side: Optional[int] = None):
        if not nexts:
            return None
        if len(nexts) == 1:
            return nexts[0]

        if side is not None:
            self.player_type = side
        color = "Black" if self.player_type == 1 else "White"
        color_text = "B" if self.player_type == 1 else "W"
        message = (
            "We will provide information about the current game board (with size 8x8), which is represented by a 64-element array called board. "
            "The positions on the board are ordered from left to right and top to bottom, where board[0] represents the top-left corner piece or space, "
            "board[7] represents the top-right corner piece or space, board[56] represents the bottom-left corner piece or space, "
            "and board[63] represents the bottom-right corner piece or space."
            "The board position is represented as follows:\n"
            "0(1A)  1(1B)  2(1C)  3(1D)  4(1E)  5(1F)  6(1G)  7(1H)\n"
            "8(2A)  9(2B)  10(2C) 11(2D) 12(2E) 13(2F) 14(2G) 15(2H)\n"
            "16(3A) 17(3B) 18(3C) 19(3D) 20(3E) 21(3F) 22(3G) 23(3H)\n"
            "24(4A) 25(4B) 26(4C) 27(4D) 28(4E) 29(4F) 30(4G) 31(4H)\n"
            "32(5A) 33(5B) 34(5C) 35(5D) 36(5E) 37(5F) 38(5G) 39(5H)\n"
            "40(6A) 41(6B) 42(6C) 43(6D) 44(6E) 45(6F) 46(6G) 47(6H)\n"
            "48(7A) 49(7B) 50(7C) 51(7D) 52(7E) 53(7F) 54(7G) 55(7H)\n"
            "56(8A) 57(8B) 58(8C) 59(8D) 60(8E) 61(8F) 62(8G) 63(8H)\n"
            "The positions 0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63, 8, 16, 24, 32, 40, 48, 15, 23, 31, 39, 47, 55 on the board are the edges of the board. "
            "On the board, there are a total of 8 columns, denoted by A to H, among which the columns represented by A and H are the edges. There are also 8 rows, denoted by 1 to 8, where 1 and 8 are the edges."
            "Black plays first, with black pieces represented by 'B', white pieces by 'W', and empty spaces by '-'. "
            "To ease your burden, we will also use a variable named nexts to tell you the available positions for placing your pieces. "
            "Note that the positions 9(2B), 14(2G), 49(7B), and 54(7G) on the board are very very dangerous, try to avoid placing your pieces there. "
            "Moreover, positions 0(1A), 7(1H), 56(8A), and 63(8H) on the board are very advantageous as they are in the four corners. "
            "Please try your best to prevent your opponent from occupying these positions, and aim to occupy them yourself."
            "Simulate various scenarios after many moves in your brain, and make your decision after careful consideration. "
            "Remember, you are a top-level player of Othello(aka Reversi), so please demonstrate the sophistication of your strategy and the depth of your thought. "
            "Understanding the importance of stable pieces and predicting and planning moves. "
            "Emphasize on creating stable pieces as a foundation for gameplay. "
        )
        message += f"You are playing {color} side, we will use {color_text} to represent your pieces.\n"
        board_status_str = self.get_board_status_str(board)
        message += f"The board status now is: board =\n{board_status_str}\n"
        next_str = self.get_next_str(nexts)

        message += f"You can only choose one of the following positions to place your piece: nexts = {next_str}\n"

        message += f"Now you are playing {color} and you should directly output {color} and the position of the move (without any analysis), for example: \"{color}: {nexts[0]}\".\n"
        # message += f"Now you are playing {color} and you should output {color} and the position of the move (explain why you choose here), for example: \"{color}: {nexts[0]}\".\n"
        # message += "If you don't understand the input, or you need to provide any additional information, or if you feel there are areas for improvement in the information given to you, you can reply with: \"Improve: your suggestions\"\n"

        if self.log_prompt:
            print(message)
        answer = self.get_chat_action(message)
        if answer is None:
            return nexts[0]
        if self.log_prompt:
            print(answer)
        # exit()
        action = re.findall(rf'{color}:\s*([0-5][0-9]|6[0-3]|[0-9])', answer)
        action = action[0]
        action = int(action)
        retry_times = 0
        while action not in nexts:
            if retry_times > 3:
                print("大模型重试次数过多，直接选择第一个可选位置！")
                return nexts[0]
            action = self.retry(message, answer, color)
            retry_times += 1
        if action is None:
            action = nexts[0]
        return action

    def web_act(self, board, nexts, side=None):
        # 黑棋先走，黑棋是action2(即agent2)，黑子在棋盘上表示为1
        if self.log_board:
            print("name: ", self.name, " board: \n", np.array(board).reshape(8, 8), " nexts: ", nexts)
        if nexts == []:
            action = None
        elif len(nexts) == 1:
            action = nexts[0]
        else:
            action = self.act(board, nexts, side=side)

        return action
