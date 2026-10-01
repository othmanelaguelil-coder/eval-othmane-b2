from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Literal

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy.exc import IntegrityError


app = FastAPI()


# DATABASE


DATABASE_URL = "sqlite:///./stations.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    status = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()



# PYDANTIC MODELS


class StationCreate(BaseModel):
    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: Literal["open", "closed", "maintenance"] = "open"


class StationPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    status: Literal["open", "closed", "maintenance"] | None = None



# ROUTES


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/stations", status_code=201)
def create_station(
    station: StationCreate,
    db: Session = Depends(get_db)
):

    new_station = Station(
        code=station.code,
        name=station.name,
        capacity=station.capacity,
        status=station.status
    )

    db.add(new_station)

    try:
        db.commit()
        db.refresh(new_station)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=409,
            detail="Code already exists"
        )

    return new_station


@app.get("/stations")
def get_stations(
    status: str | None = None,
    db: Session = Depends(get_db)
):

    if status is not None:
        return db.query(Station).filter(
            Station.status == status
        ).all()

    return db.query(Station).all()


@app.get("/stations/{station_id}")
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):

    station = db.query(Station).filter(
        Station.id == station_id
    ).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return station


@app.patch("/stations/{station_id}")
def update_station(
    station_id: int,
    data: StationPatch,
    db: Session = Depends(get_db)
):

    station = db.query(Station).filter(
        Station.id == station_id
    ).first()

    if station is None:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    if data.name is not None:
        station.name = data.name

    if data.status is not None:
        station.status = data.status

    db.commit()
    db.refresh(station)

    return station