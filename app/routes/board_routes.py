from flask import Blueprint, request, Response
from app.models.board import Board
from app.models.card import Card
from .route_utilities import validate_model, create_model
from ..db import db
from datetime import date
import os
import requests

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():
    boards = Board.query.all()
    return [board.to_dict() for board in boards], 200

@bp.post("")
def create_board():
    data = request.get_json()
    board, status = create_model(Board, data)
    return board.to_dict(), status

@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model(Board, board_id)
    return board.to_dict(), 200

@bp.get("/<board_id>/cards")
def get_board_cards(board_id):
    board = validate_model(Board, board_id)
    cards = [card.to_dict() for card in board.cards]
    return cards, 200

# Create a new card on a board
@bp.post("/<board_id>/cards")
def add_card_to_board(board_id):
    board = validate_model(Board, board_id)
    data = request.get_json()
    data["board_id"] = board.board_id
    card, status = create_model(Card, data)
    return card.to_dict(), status

# Delete one board
@bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_model(Board, board_id)

    db.session.delete(board)
    db.session.commit()

    return Response(status=204, mimetype="application/json")
