from sqlalchemy.orm import Session

from app import models, schemas
from app.scoring import calculate_viral_score


def create_creator(db: Session, creator: schemas.CreatorCreate) -> models.Creator:
    db_creator = models.Creator(**creator.model_dump())
    db.add(db_creator)
    db.commit()
    db.refresh(db_creator)
    return db_creator


def get_creators(db: Session) -> list[models.Creator]:
    return db.query(models.Creator).order_by(models.Creator.created_at.desc()).all()


def get_creator(db: Session, creator_id: int) -> models.Creator | None:
    return db.query(models.Creator).filter(models.Creator.id == creator_id).first()


def delete_creator(db: Session, creator_id: int) -> bool:
    creator = get_creator(db, creator_id)
    if creator is None:
        return False

    db.delete(creator)
    db.commit()
    return True


def create_clip(db: Session, clip: schemas.ClipCreate) -> models.Clip:
    clip_data = clip.model_dump()
    clip_data["viral_score"] = calculate_viral_score(
        views=clip.views,
        likes=clip.likes,
        comments=clip.comments,
    )
    db_clip = models.Clip(**clip_data)
    db.add(db_clip)
    db.commit()
    db.refresh(db_clip)
    return db_clip


def get_clips(db: Session) -> list[models.Clip]:
    return db.query(models.Clip).order_by(models.Clip.viral_score.desc()).all()


def get_trending_clips(db: Session) -> list[models.Clip]:
    return (
        db.query(models.Clip)
        .filter(models.Clip.viral_score >= 75)
        .order_by(models.Clip.viral_score.desc())
        .all()
    )


def get_creator_clips(db: Session, creator_id: int) -> list[models.Clip]:
    return (
        db.query(models.Clip)
        .filter(models.Clip.creator_id == creator_id)
        .order_by(models.Clip.viral_score.desc())
        .all()
    )


def get_clip(db: Session, clip_id: int) -> models.Clip | None:
    return db.query(models.Clip).filter(models.Clip.id == clip_id).first()


def delete_clip(db: Session, clip_id: int) -> bool:
    clip = get_clip(db, clip_id)
    if clip is None:
        return False

    db.delete(clip)
    db.commit()
    return True
