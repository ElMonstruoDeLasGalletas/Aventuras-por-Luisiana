from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..models import Review, User, Route
from ..schemas import ReviewCreate, ReviewOut, ReviewUpdate

def _get_review_or_404(db: Session, review_id: int) -> Review:
    review = (
        db.query(Review)
        .filter(Review.id == review_id, Review.is_deleted == False)  # noqa
        .first()
    )
    if not review:
        raise HTTPException(404, "Review not found")
    return review

def create_review(db: Session, data: ReviewCreate, user: User) -> Review:

    review = review(
        user_id=data.user_id,
        route_id=data.route_id,
        rating=data.rating,
        content=data.content,
        is_deleted=data.is_deleted
    )

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def list_reviews(
    route_id: int,
    db: Session,
):
    return (
            db.query(Review)
            .filter(Review.route_id == route_id, Review.is_deleted == False) #noqa
            .order_by(Review.id.desc())
            .limit(200)
            .all()
        )


def get_review(db: Session, review_id: int) -> Review:
    return _get_review_or_404(db, review_id)


def update_review(
    db: Session,
    review_id: int,
    data: ReviewUpdate,
    user: User,
) -> Review:
    review = _get_review_or_404(db, review_id)

    payload = data.model_dump(exclude_unset=True)

    for field, value in payload.items():
        setattr(review, field, value)

    db.commit()
    db.refresh(review)
    return review


def delete_review(
    db: Session,
    review_id: int,
    user: User,
) -> None:
    review = _get_review_or_404(db, review_id)

    review.is_deleted = True
    db.commit()
