from app.models.board import Board
from app.models.card import Card
from app.db import db
import pytest

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_boards_one_saved_boards(client, one_board):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "board_id": 1,
            "title": "Board 1",
            "owner": "Jeslyn"
        }
    ]

def test_get_board(client, one_board):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
            "board_id": 1,
            "title": "Board 1",
            "owner": "Jeslyn"
        }

def test_get_board_not_found(client):
    # Act
    response = client.get("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}

def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "A Brand New board",
        "owner": "Test owner",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
            "board_id": 1,
            "title": "A Brand New board",
            "owner": "Test owner"
        }

    query = db.select(Board).where(Board.board_id == 1)
    new_board = db.session.scalar(query)

    assert new_board
    assert new_board.title == "A Brand New board"
    assert new_board.owner == "Test owner"

def test_delete_board(client, one_board):
    # Act
    response = client.delete("/boards/1")

    # Assert
    assert response.status_code == 204

    query = db.select(Board).where(Board.board_id == 1)
    assert db.session.scalar(query) == None

def test_delete_board_not_found(client):
    # Act
    response = client.delete("/boards/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert db.session.scalars(db.select(Board)).all() == []
    assert response_body == {"message": "Board 1 not found"}

def test_create_board_must_contain_owner(client):
    # Act
    response = client.post("/boards", json={
        "owner": "Test User"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert db.session.scalars(db.select(Board)).all() == []

def test_create_board_must_contain_title(client):
    # Act
    response = client.post("/boards", json={
        "title": "Test Title"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
    assert db.session.scalars(db.select(Board)).all() == []

def test_get_cards_for_specific_board(client, one_card_belongs_to_one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
            {
                "id": 1,
                "board_id": 1,
                "card_message": "Card 1",
                "likes": 0,
                "dislikes": 0
            }
        ]

def test_get_cards_for_specific_board_no_cards(client, one_board):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 0
    assert response_body == []

def test_get_cards_for_specific_board_no_board(client):
    # Act
    response = client.get("/boards/1/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}

def test_post_card_to_board(client, one_board):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "New card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "board_id": 1,
        "card_message": "New card",
        "likes": 0,
        "dislikes": 0
    }

    query = db.select(Card).where(Card.card_id == 1)
    new_card = db.session.scalar(query)
    assert new_card
    assert new_card.message == "New card"
    assert new_card.board_id == 1

def test_post_card_to_board_not_found(client):
    # Act
    response = client.post("/boards/1/cards", json={
        "message": "New card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Board 1 not found"}

def test_post_card_to_board_already_with_cards(client, one_card_belongs_to_one_board):
    response = client.post("/boards/1/cards", json={
        "message": "Second card"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 2,
        "board_id": 1,
        "card_message": "Second card",
        "likes": 0,
        "dislikes": 0
    }

    query = db.select(Card).where(Card.card_id == 2)
    new_card = db.session.scalar(query)
    assert new_card
    assert new_card.message == "Second card"
    assert new_card.board_id == 1

    # Check if the board has 2 cards
    board_query = db.select(Board).where(Board.board_id == 1)
    board = db.session.scalar(board_query)
    assert len(board.cards) == 2
