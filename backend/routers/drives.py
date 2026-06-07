import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


@router.get("/offense")
def drive_offense(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_drive_scoring_stats(conn))


@router.get("/offense/finishers")
def drive_finishers(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_drive_finishers(conn))


@router.get("/defense")
def drive_defense(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_drive_scoring_stats(conn))


@router.get("/defense/beaten")
def defenders_beaten(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_defenders_beaten_off_dribble(conn))
