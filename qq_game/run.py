# -*- coding: utf-8 -*-

from qq_game_spector import Spector
from agent_controller import GameController

if __name__ == '__main__':
    Spector(GameController(auto_start=True)).run()
