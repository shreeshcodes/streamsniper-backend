from datetime import datetime, timedelta, timezone

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StreamSniper API",
    description="Backend MVP for finding and ranking viral creator clips.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def seed_demo_data() -> None:
    db = next(get_db())
    try:
        if db.query(models.Creator).first():
            return

        now = datetime.now(timezone.utc)
        creators = [
            models.Creator(name="Kai Cenat", platform="Twitch", handle="@kaicenat"),
            models.Creator(name="IShowSpeed", platform="YouTube", handle="@IShowSpeed"),
            models.Creator(name="xQc", platform="Twitch", handle="@xQc"),
            models.Creator(name="Adin Ross", platform="Kick", handle="@adinross"),
            models.Creator(name="Hasan", platform="Twitch", handle="@hasanabi"),
        ]
        db.add_all(creators)
        db.commit()

        for creator in creators:
            db.refresh(creator)

        sample_clips = [
            {
                "creator_id": creators[0].id,
                "title": "Kai turns a quiet stream into a full chat takeover",
                "platform": "Twitch",
                "url": "https://example.com/clips/kai-chat-takeover",
                "thumbnail_url": "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?auto=format&fit=crop&w=1200&q=80",
                "views": 685000,
                "likes": 48000,
                "comments": 5600,
                "posted_at": now - timedelta(hours=4),
            },
            {
                "creator_id": creators[1].id,
                "title": "Speed's impossible reaction lands everywhere in one hour",
                "platform": "YouTube",
                "url": "https://example.com/clips/speed-impossible-reaction",
                "thumbnail_url": "https://images.unsplash.com/photo-1511512578047-dfb367046420?auto=format&fit=crop&w=1200&q=80",
                "views": 920000,
                "likes": 72000,
                "comments": 9400,
                "posted_at": now - timedelta(hours=2),
            },
            {
                "creator_id": creators[2].id,
                "title": "xQc speedruns the worst possible decision",
                "platform": "Twitch",
                "url": "https://example.com/clips/xqc-worst-decision",
                "thumbnail_url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1200&q=80",
                "views": 410000,
                "likes": 26500,
                "comments": 3100,
                "posted_at": now - timedelta(hours=7),
            },
            {
                "creator_id": creators[3].id,
                "title": "Adin's guest reveal spikes the whole stream",
                "platform": "Kick",
                "url": "https://example.com/clips/adin-guest-reveal",
                "thumbnail_url": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=1200&q=80",
                "views": 275000,
                "likes": 18500,
                "comments": 2200,
                "posted_at": now - timedelta(hours=11),
            },
            {
                "creator_id": creators[4].id,
                "title": "Hasan breaks down the headline everyone is clipping",
                "platform": "Twitch",
                "url": "https://example.com/clips/hasan-headline-breakdown",
                "thumbnail_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
                "views": 195000,
                "likes": 12100,
                "comments": 1800,
                "posted_at": now - timedelta(hours=16),
            },
            {
                "creator_id": creators[0].id,
                "title": "Kai's lobby moment gets clipped before the round ends",
                "platform": "Twitch",
                "url": "https://example.com/clips/kai-lobby-moment",
                "thumbnail_url": "https://images.unsplash.com/photo-1560253023-3ec5d502959f?auto=format&fit=crop&w=1200&q=80",
                "views": 135000,
                "likes": 8200,
                "comments": 900,
                "posted_at": now - timedelta(days=1, hours=3),
            },
        ]

        for clip in sample_clips:
            crud.create_clip(db, schemas.ClipCreate(**clip))
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    seed_demo_data()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "StreamSniper API is running"}


@app.post("/creators", response_model=schemas.Creator, status_code=status.HTTP_201_CREATED)
def create_creator(creator: schemas.CreatorCreate, db: Session = Depends(get_db)):
    return crud.create_creator(db=db, creator=creator)


@app.get("/creators", response_model=list[schemas.Creator])
def read_creators(db: Session = Depends(get_db)):
    return crud.get_creators(db=db)


@app.get("/creators/{creator_id}", response_model=schemas.Creator)
def read_creator(creator_id: int, db: Session = Depends(get_db)):
    creator = crud.get_creator(db=db, creator_id=creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    return creator


@app.delete("/creators/{creator_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_creator(creator_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_creator(db=db, creator_id=creator_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Creator not found")


@app.post("/clips", response_model=schemas.Clip, status_code=status.HTTP_201_CREATED)
def create_clip(clip: schemas.ClipCreate, db: Session = Depends(get_db)):
    creator = crud.get_creator(db=db, creator_id=clip.creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    return crud.create_clip(db=db, clip=clip)


@app.get("/clips", response_model=list[schemas.Clip])
def read_clips(db: Session = Depends(get_db)):
    return crud.get_clips(db=db)


@app.get("/clips/trending", response_model=list[schemas.Clip])
def read_trending_clips(db: Session = Depends(get_db)):
    return crud.get_trending_clips(db=db)


@app.get("/creators/{creator_id}/clips", response_model=list[schemas.Clip])
def read_creator_clips(creator_id: int, db: Session = Depends(get_db)):
    creator = crud.get_creator(db=db, creator_id=creator_id)
    if creator is None:
        raise HTTPException(status_code=404, detail="Creator not found")
    return crud.get_creator_clips(db=db, creator_id=creator_id)


@app.delete("/clips/{clip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clip(clip_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_clip(db=db, clip_id=clip_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Clip not found")
