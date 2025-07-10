<<<<<<< HEAD
import pytest
from app.models.board import Board
from app.db import db


def test_create_board(client):
    # Act
    response = client.post("/boards", json={
        "title": "Inspo Wall",
        "owner": "Jamie"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "title" in response_body
    assert "owner" in response_body
    assert "board_id" in response_body
    assert response_body == {
        "board_id": response_body["board_id"],
        "title": "Inspo Wall",
        "owner": "Jamie"
    }


def test_get_all_boards(client):
    # Arrange
    board1 = Board(title="Board One", owner="Daffy")
    board2 = Board(title="Board Two", owner="Duck")
    db.session.add_all([board1, board2])
    db.session.commit()

=======
from app.models.board import Board
from app.models.card import Card
from app.db import db
import pytest

def test_get_boards_no_saved_boards(client):
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
<<<<<<< HEAD
    assert isinstance(response_body, list)
    assert len(response_body) >= 2
    titles = [board["title"] for board in response_body]
    assert "Board One" in titles
    assert "Board Two" in titles


def test_get_one_board(client):
    # Arrange
    board = Board(title="Test Board", owner="Tester")
    db.session.add(board)
    db.session.commit()

    # Act
    response = client.get(f"/boards/{board.board_id}")
=======
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
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
<<<<<<< HEAD
        "board_id": board.board_id,
        "title": "Test Board",
        "owner": "Tester"
    }


def test_get_cards_from_board_returns_empty_list(client):
    # Arrange
    board = Board(title="Empty Board", owner="Nobody")
    db.session.add(board)
    db.session.commit()

    # Act
    response = client.get(f"/boards/{board.board_id}/cards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_delete_board(client):
    # Arrange
    board = Board(title="Delete Me", owner="Someone")
    db.session.add(board)
    db.session.commit()

    # Act
    response = client.delete(f"/boards/{board.board_id}")
=======
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
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40

    # Assert
    assert response.status_code == 204

<<<<<<< HEAD
    # Confirm board is gone
    get_response = client.get(f"/boards/{board.board_id}")
    assert get_response.status_code == 404
=======
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
>>>>>>> 011728445acc1bc633bf89f7e7ebe46b557aba40
