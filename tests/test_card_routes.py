import pytest
from app.models.card import Card
from app.db import db

def test_delete_card(client, one_card):
    # Act
    response = client.delete("/cards/1")

    # Assert
    assert response.status_code == 204

    # Check if the card was deleted
    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    assert card is None

def test_delete_card_not_found(client):
    # Act
    response = client.delete("/cards/1")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Card 1 not found"}

def test_liked_card(client, one_card):
    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    initial_likes = card.likes_count
    
    # Like the card
    response = client.patch("/cards/1/like")
    assert response.status_code == 200
    response_body = response.get_json()
    assert response_body["likes"] == initial_likes + 1

    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    assert card.likes_count == initial_likes + 1

def test_liked_card_multiple_times(client, one_card):
    response1 = client.patch("/cards/1/like")
    assert response1.status_code == 200
    assert response1.get_json()["likes"] == 1
    
    response2 = client.patch("/cards/1/like")
    assert response2.status_code == 200
    assert response2.get_json()["likes"] == 2
    
    response3 = client.patch("/cards/1/like")
    assert response3.status_code == 200
    assert response3.get_json()["likes"] == 3

    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    assert card.likes_count == 3

def test_disliked_card(client, one_card):
    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    initial_dislikes = card.dislike_count
    
    # Dislike the card
    response = client.patch("/cards/1/dislike")
    assert response.status_code == 200
    response_body = response.get_json()
    assert response_body["dislikes"] == initial_dislikes + 1

    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    assert card.dislike_count == initial_dislikes + 1

def test_disliked_card_multiple_times(client, one_card):
    response1 = client.patch("/cards/1/dislike")
    assert response1.status_code == 200
    assert response1.get_json()["dislikes"] == 1
    
    response2 = client.patch("/cards/1/dislike")
    assert response2.status_code == 200
    assert response2.get_json()["dislikes"] == 2
    
    response3 = client.patch("/cards/1/dislike")
    assert response3.status_code == 200
    assert response3.get_json()["dislikes"] == 3

    query = db.select(Card).where(Card.card_id == 1)
    card = db.session.scalar(query)
    assert card.dislike_count == 3