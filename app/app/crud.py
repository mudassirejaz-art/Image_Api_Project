from sqlalchemy.orm import Session
from .models import SavedImage

def like_image(db: Session, image_url: str):
    img = db.query(SavedImage).filter(SavedImage.image_url==image_url).first()
    if not img:
        img = SavedImage(image_url=image_url, liked=True)
        db.add(img)
    else:
        img.liked = True
    db.commit()
    return img

def save_image(db: Session, image_url: str, photographer: str):
    img = db.query(SavedImage).filter(SavedImage.image_url==image_url).first()
    if not img:
        img = SavedImage(image_url=image_url, photographer=photographer, saved=True)
        db.add(img)
    else:
        img.saved = True
    db.commit()
    return img
