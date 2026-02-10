from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..deps import get_db, get_current_user
from ..models import User, Route
from ..schemas import ReviewCreate, ReviewOut, ReviewUpdate
from ..services import review_service

router = APIRouter(prefix="", tags=["reviews"])

@router.post("/route/{route_id}/reviews", response_model=ReviewOut)
def create_review(
    route_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    route = db.query(Route).filter(
        Route.id == route_id,
        Route.is_deleted == False
    ).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    return review_service.create_review(db, data, current_user)

@router.get("/route/{route_id}/reviews", response_model=List[ReviewOut])
def get_reviews(
    route_id: int,
    db: Session = Depends(get_db),
):
    return review_service.list_reviews(route_id, db)

@router.get("/user", response_model=list[ReviewOut])
def get_reviews_from_user(
    user_id: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return review_service.get_reviews_from_user(db, user_id.id)

@router.get("/reviews/{review_id}", response_model=ReviewOut)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):
    return review_service.get_review(db, review_id)

@router.put("/{review_id}", response_model=ReviewOut)
def update_review(
    review_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return review_service.update_review(db, review_id, data, current_user)

@router.delete("/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    review_service.delete_review(db, review_id, current_user)
    return None
