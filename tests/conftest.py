import pytest
<<<<<<< HEAD
from app import create_app, db

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })
=======
from app import create_app
from app.db import db
from flask.signals import request_finished
from dotenv import load_dotenv
import os
from app.models.board import Board
from app.models.card import Card

load_dotenv()

@pytest.fixture
def app():
    # create the app with a test configuration
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40

    with app.app_context():
        db.create_all()
        yield app
<<<<<<< HEAD
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
=======

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    new_board = Board(title="Board 1", 
                    owner="Jeslyn")
    db.session.add(new_board)
    db.session.commit()
    return new_board

@pytest.fixture
def one_card(app, one_board):
    new_card = Card(message="Card 1", board_id=one_board.board_id)
    db.session.add(new_card)
    db.session.commit()
    return new_card

@pytest.fixture
def one_card_belongs_to_one_board(app, one_board, one_card):
    card_query = db.select(Card).where(Card.card_id == 1)
    board_query = db.select(Board).where(Board.board_id == 1)
    card = db.session.scalar(card_query)
    board = db.session.scalar(board_query)
    board.cards.append(card)
    db.session.commit()
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40
