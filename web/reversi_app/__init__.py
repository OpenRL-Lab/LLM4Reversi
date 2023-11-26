from flask import Blueprint

reversi_app = Blueprint('reversi_app', __name__)

from reversi_app import views
