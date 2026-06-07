import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


@router.get("/offense")
def pnr_offense(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_offense_roll_and_pop_stats(conn))


@router.get("/defense/screen-breakdown")
def screen_defense_breakdown(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_screen_defense_breakdown(conn))


@router.get("/defense/roll-coverage")
def roll_defensive_coverage(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_roll_defensive_coverage(conn))


@router.get("/defense/pop-coverage")
def pop_defensive_coverage(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_pop_defensive_coverage(conn))
