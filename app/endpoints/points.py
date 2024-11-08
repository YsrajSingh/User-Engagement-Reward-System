from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from models.users import Users
from models.points import Points
from schemas.points import PointsCreate, PointsResponse, PointOut
from models import get_db
from typing import List
from fastapi_pagination import Page, paginate
from utils.helper import get_current_user
from fastapi_pagination.ext.sqlalchemy import paginate as paginate_sqlalchemy
from sqlalchemy import func



router = APIRouter(prefix="", tags=["Points"])


@router.post("/points", response_model=PointsResponse)
def add_points(
    points_data: PointsCreate,
    session: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    # Create points entry
    points_entry = Points(user_id=current_user.id, points=points_data.points, description=points_data.description)
    session.add(points_entry)

    # Update user's total points
    current_user.total_points += points_data.points
    session.commit()
    session.refresh(points_entry)

    return points_entry


@router.get("/points")
async def get_points(
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),  # default to 10, minimum 1
    offset: int = Query(0, ge=0),  # default to 0, minimum 0
):
    # Querying the Points table with limit and offset
    points_query: Query = db.query(Points).offset(offset).limit(limit)
    # Get total count for pagination
    total_count = db.query(func.count(Points.id)).scalar()

    # Fetch the paginated results
    points = points_query.all()

    # Return the paginated results with total count
    return {
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
        "points": points,
    }