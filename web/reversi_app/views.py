from flask import request, jsonify, g
from reversi_app import reversi_app
from reversi_app.utils import myRender

from reversi_tool.agents.web_white import WhiteSideAgent
from reversi_tool.agents.web_black import BlackSideAgent

agent1 = WhiteSideAgent()
agent2 = BlackSideAgent()


@reversi_app.route('/get_action1', methods=['GET', 'POST'])
def get_action1():
    board = request.json['board']
    nexts = request.json['nexts']
    action = agent1.web_act(board, nexts)
    json_data = {'action': action}
    print("return action1: ", action)
    return jsonify(json_data)


@reversi_app.route('/get_action2', methods=['GET', 'POST'])
def get_action2():
    board = request.json['board']
    nexts = request.json['nexts']
    action = agent2.web_act(board, nexts)
    json_data = {'action': action}
    print("return action2: ", action)
    return jsonify(json_data)


@reversi_app.route('/index.html')
@reversi_app.route('')
@reversi_app.route('/')
def index():
    print('__name__', __name__)
    return myRender(__name__, 'index.html')
