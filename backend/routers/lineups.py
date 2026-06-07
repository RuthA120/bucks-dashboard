import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


@router.get("/mil/offense")
def mil_lineup_offense(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_mil_lineup_offense(conn))


@router.get("/mil/defense")
def mil_lineup_defense(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_mil_lineup_defense(conn))

@router.get("/mil/player-keys")
def mil_lineup_player_keys(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_mil_lineup_player_keys(conn))