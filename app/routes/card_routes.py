from flask import Blueprint, request, Response
from app.models.card import Card
from .route_utilities import validate_model
from ..db import db
from datetime import date

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.patch("/<card_id>/like")
def like_card(card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1
    db.session.commit()
    return card.to_dict(), 200