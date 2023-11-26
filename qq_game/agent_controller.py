import time

from pynput.mouse import Button, Controller

from reversi_tool.agents.qq_game_agent import QQGameAgent as Agent

from utils.map import Map

row_cha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']


class GameController:
    def __init__(self, auto_start, p_resize=1.0, alg=None):
        self.auto_start = auto_start
        self.p_resize = p_resize
        self.mouse = Controller()

        self.pre_M = None
        self.pre_role = None
        self.agent = Agent()

    def click_position(self, position):
        before_position = self.get_position()
        self.move_to(position)
        self.mouse.click(Button.left, 1)
        self.move_to(before_position)

    def move_to(self, position):
        self.mouse.position = position

    def get_position(self):
        return self.mouse.position

    def run(self, state, board, M, board_rect, role_info):
        if state == 'to_prepare' and self.auto_start:
            self.prepare(board_rect)

        if state == 'in_board' and role_info[1]:
            if role_info[0]:
                my_role = 1
            else:
                my_role = -1

            if not (self.pre_M is None) and (self.pre_M == M).all() and self.pre_role == my_role:
                self.perform_action(self.pre_action, board_rect)
                return
            m = self.newMap(M, my_role)
            self.pre_M = M
            self.pre_role = my_role

            # print('next step number:{}'.format(m.nextNum))
            m.show()

            if m.nextNum == 0:
                print('没有地方可以下子！')
                return

            s_t = time.time()
            print("智能体思考当中...")
            action = self.agent.web_act(m.board, m.nextIndex, side=m.side)
            # print("action", action)
            # action = action[0] * 8 + action[1]
            # print("action", action)
            self.pre_action = action

            print(
                '智能体运行花费:{:.3f}秒 智能体输出动作为:{}'.format(time.time() - s_t,
                                                                     [int(action / 8) + 1, row_cha[int(action % 8)]]))
            self.perform_action(action, board_rect)

    def newMap(self, M, my_role):
        m = Map()
        for i in range(8):
            for j in range(8):
                m[i * 8 + j] = M[i, j]
        m.side = my_role
        m.update()
        return m

    def perform_action(self, action, board_rect):
        action = [int(action / 8), int(action % 8)]
        # start = [259, 273]
        # shift = 70

        start = [290, 310]
        shift = 80

        w = board_rect[2] + start[1] + shift * action[1]
        h = board_rect[0] + start[0] + shift * action[0]
        w /= self.p_resize
        h /= self.p_resize
        position = [w, h]

        self.click_position(position)
        time.sleep(2)

    def prepare(self, board_rect):
        # w_offset = 500
        # h_offset = 873
        w_offset = 600
        h_offset = 1050
        # position = [(board_rect[2] + w_offset) / 1.25, (board_rect[0] + h_offset) / 1.25]
        position = [board_rect[2] + w_offset, board_rect[0] + h_offset]
        self.click_position(position)
        print('已自动点击准备按钮！')
