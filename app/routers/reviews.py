from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..deps import get_db, get_current_user
from ..models import Review, User, Route
from ..schemas import ReviewCreate, ReviewOut, ReviewUpdate
from ..services import review_service

router = APIRouter(prefix="/route/{route_id}/reviews", tags=["reviews"])

@router.post("", response_model=ReviewOut)
def create_review(
    route_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    route = db.query(Route).filter(Route.id==route_id, Route.is_deleted==False).first() #noqa
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    review = review_service.create_review(db, data, current_user)
    return review

@router.get("", response_model=List[ReviewOut])
def list_reviews(
    route_id: int,
    db: Session = Depends(get_db),
):
    reviews = review_service.list_reviews(route_id, db)
    if reviews == []:
        raise HTTPException(status_code=404, detail="Reviews not found")
    
    return reviews

@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = review_service.get_review(db, review_id)  # noqa
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewOut)
def update_reviews_endreviewsnt(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.update_review(db, review_id, data, current_user)


@router.delete("/{review_id}", status_code=204)
def delete_review_endreviewnt(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review_service.delete_reviews(db, review_id, current_user)
    return None