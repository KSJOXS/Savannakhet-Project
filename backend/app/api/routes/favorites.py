from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["Favorites"])


@router.post("/favorites/toggle")
def toggle_favorite(data: schemas.FavoriteToggle, db: Session = Depends(get_db)):
    place = db.query(models.Place).filter(
        models.Place.id == data.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found.")

    fav = db.query(models.Favorite).filter(
        models.Favorite.user_id == data.user_id,
        models.Favorite.place_id == data.place_id
    ).first()

    if fav:
        db.delete(fav)
        db.commit()
        return {"status": "removed", "place_id": data.place_id}
    else:
        new_fav = models.Favorite(user_id=data.user_id, place_id=data.place_id)
        db.add(new_fav)
        db.commit()
        return {"status": "added", "place_id": data.place_id}


@router.get("/users/{user_id}/favorites", response_model=list[schemas.FavoriteResponse])
def get_user_favorites(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Favorite).filter(models.Favorite.user_id == user_id).all()
