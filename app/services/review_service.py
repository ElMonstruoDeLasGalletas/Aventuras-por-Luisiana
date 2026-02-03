from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import Review, User
from ..schemas import ReviewCreate, ReviewUpdate

def _get_review_or_404(db: Session, review_id: int) -> Review:
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.is_deleted == False
    ).first()
    if not review:
        raise HTTPException(404, "Review not found")
    return review

def create_review(db: Session, data: ReviewCreate, user: User) -> Review:
    review = Review(
        user_id=user.id,
        route_id=data.route_id,
        rating=data.rating,
        content=data.content,
        is_deleted=False
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def list_reviews(route_id: int, db: Session):
    return db.query(Review).filter(
        Review.route_id == route_id,
        Review.is_deleted == False
    ).order_by(Review.id.desc()).all()

def get_review(db: Session, review_id: int) -> Review:
    return _get_review_or_404(db, review_id)

def update_review(db: Session, review_id: int, data: ReviewUpdate) -> Review:
    review = _get_review_or_404(db, review_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review

def delete_review(db: Session, review_id: int):
    review = _get_review_or_404(db, review_id)
    review.is_deleted = True
    db.commit()
