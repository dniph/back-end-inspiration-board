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

    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
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
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
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

    # Assert
    assert response.status_code == 204

    # Confirm board is gone
    get_response = client.get(f"/boards/{board.board_id}")
    assert get_response.status_code == 404