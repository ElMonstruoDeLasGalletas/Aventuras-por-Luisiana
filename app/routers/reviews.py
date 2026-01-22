from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..models import Review, User, POI
from ..schemas import ReviewCreate, ReviewOut

router = APIRouter(prefix="/pois/{poi_id}/reviews", tags=["reviews"])

@router.post("", response_model=ReviewOut)
def create_review(
    poi_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    poi = db.query(POI).filter(POI.id==poi_id, POI.is_deleted==False).first() #noqa
    if not poi:
        raise HTTPException(status_code=404, detail="POI not found")

    review = Review(
        user_id=data.user_id,
        poi_id=data.poi_id,
        rating=data.rating,
        content=data.content,
        is_deleted=data.is_deleted
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

@router.get("", response_model=List[ReviewOut])
def list_reviews(
    poi_id: int,
    db: Session = Depends(get_db),
):
    return (
            db.query(Review)
            .filter(Review.poi_id == poi_id, Review.is_deleted == False) #noqa
            .order_by(Review.id.desc())
            .limit(200)
            .all()
        )

@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id, Review.is_deleted == False).first()  # noqa
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review
