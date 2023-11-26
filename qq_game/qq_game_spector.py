import time
import platform
import pyautogui
import aircv as ac

import numpy as np

white_thr = 600
black_thr = 150
STATEs = ['nothing', 'no_enemy', 'to_prepare', 'rival_to_prepare', 'rival_turn', 'own_turn']


class Spector():
    def __init__(self, controller=None):
        assert platform.system() == 'Windows', "目前只支持Windows系统"
        d_r = 'images/'
        logo_name = d_r + 'logo.png'
        begin_name = d_r + 'begin.png'
        self.logo = ac.imread(logo_name)
        self.begin = ac.imread(begin_name)
        self.time_zeros = [[ac.imread(d_r + 'left_zero2.png'), ac.imread(d_r + 'right_zero2.png')],
                           [ac.imread(d_r + 'left_zero.png'), ac.imread(d_r + 'right_zero.png')]]
        self.empty_en = ac.imread(d_r + 'empty_enemy.png')
        self.w = 2560
        self.h = 1440
        self.tmp_index = 0
        self.reset()
        self.controller = controller

        # 获取屏幕的宽度和高度
        screen_width, screen_height = pyautogui.size()

        print(f"屏幕分辨率：宽度 = {screen_width}, 高度 = {screen_height}")
        assert screen_width == 2560 and screen_height == 1440, "屏幕分辨率不是2560x1440，而且需要在设置-系统-屏幕-缩放和布局中将缩放设置为150%"

    def reset(self):
        self.M = None
        self.board = None
        self.board_rect = None
        self.state = 'nothing'
        self.role_info = None
        self.need_controller = False

    def run(self):
        while True:
            self.update_info()

    def update_info(self):
        tmp_file = 'screenshot_{}.png'.format(self.tmp_index)
        # tmp_file = 'images/badcase.png'
        self.window_capture(tmp_file)
        self.get_info(tmp_file)
        self.tmp_index = (self.tmp_index + 1) % 5
        if self.need_controller and self.controller is not None:
            self.controller.run(self.state, self.board, self.M, self.board_rect, self.role_info)

    def get_info(self, tmp_file):
        img = ac.imread(tmp_file)
        re = ac.find_template(img, self.logo)

        extend_w = 40
        extend_h = 900
        if re and re['confidence'] > 0.95:
            rectangle = re['rectangle']

            if rectangle[0][1] - extend_w >= 0 and rectangle[1][1] + extend_h < self.h and rectangle[0][0] >= 0 and \
                    rectangle[2][
                        0] < self.w:
                self.board_rect = (
                    rectangle[0][1] - extend_w, rectangle[1][1] + extend_h, rectangle[0][0], rectangle[2][0])
                self.board = img[rectangle[0][1] - extend_w:rectangle[1][1] + extend_h, rectangle[0][0]:rectangle[2][0],
                             ::-1]
                # import cv2
                # cv2.imwrite('saved_board.png', cv2.cvtColor(self.board, cv2.COLOR_BGR2RGB))
                if self.check_begin(self.board):
                    state_now = 'to_prepare'
                    self.need_controller = True
                    print("还在准备当中...")
                else:
                    if self.check_time_zero(self.board):
                        state_now = self.state
                        if self.state == "to_prepare":
                            state_now = 'rival_to_prepare'
                        # print("double zero time")
                        if not self.check_enemy(self.board):
                            state_now = 'no_enemy'
                            print("还没有对方玩家。 程序等待4秒！")
                            time.sleep(4)
                        else:
                            time.sleep(2)
                    else:
                        find_one = self.get_matrix()

                        if find_one:
                            state_now = 'in_board'
                        else:
                            if self.check_enemy(self.board):
                                state_now = 'rival_to_prepare'
                            else:
                                state_now = 'no_enemy'
            else:
                state_now = 'nothing'
        else:
            state_now = 'nothing'

        if state_now != self.state:
            self.need_controller = True
            self.state = state_now
            print('State is changed to {}.'.format(self.state))
            if state_now == 'nothing':
                self.reset()

    def check_enemy(self, board):
        re = ac.find_template(board, self.empty_en)

        if re and re['confidence'] > 0.97:
            return False
        else:
            return True

    def get_matrix(self):
        M = np.zeros((8, 8))
        img = self.board
        if img is None:
            self.M = None
            return
        # start = [259, 273]
        # start = [290, 310]
        start = [300, 325]
        # shift = 70
        # shift_j = 70

        shift = shift_j = 80

        white_num = 0
        black_num = 0
        for i in range(8):
            for j in range(8):
                now_point = [int(start[0] + shift * i), int(start[1] + shift_j * j)]

                if sum(img[now_point[0], now_point[1]]) > white_thr:
                    M[i, j] = -1
                    white_num += 1
                if sum(img[now_point[0], now_point[1]]) < black_thr:
                    M[i, j] = 1
                    black_num += 1

        if (self.M is None or (self.M != M).any()) and (white_num > 0 or black_num > 0):
            self.need_controller = True
            self.M = M
            left_white, my_turn = self.get_role(self.board)

            if my_turn:
                if left_white:
                    color = "AI下黑棋"
                else:
                    color = "AI下白棋"
                print('该AI下棋！ ' + color)
            else:
                if left_white:
                    color = "对方下白棋"
                else:
                    color = "对方下黑棋"
                print('该对方玩家下棋！ ' + color)
            # if left_white:
            #     print('white:{} black:{}'.format(white_num, black_num))
            # else:
            #     print('black:{} white:{}'.format(black_num, white_num))
            # print(self.M)
        return white_num > 0 or black_num > 0

    def get_role(self, board):  # True for left white, own = black
        left_white = False
        my_turn = False
        # if sum(board[517, 28]) > white_thr:
        if sum(board[610, 30]) > white_thr:
            left_white = True

        # print(board[551, 910])
        if sum(board[655, 1010]) > 540:
            my_turn = True
        self.role_info = (left_white, my_turn)
        # print("left_white:",left_white, "my_turn",my_turn)
        return left_white, my_turn

    def check_begin(self, board):
        begin_re = ac.find_template(board, self.begin)
        if begin_re and begin_re['confidence'] > 0.95:
            return True
        else:
            return False

    def window_capture(self, filename):
        # 截取全屏
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        time.sleep(0.5)

    def check_time_zero(self, board):

        for time_zeros0 in self.time_zeros:
            zero_num = 0
            # cc = []
            for time_zero in time_zeros0:
                re = ac.find_template(board, time_zero)
                if re and re['confidence'] > 0.97:
                    zero_num += 1
            if zero_num == 2:
                return True
        return False
