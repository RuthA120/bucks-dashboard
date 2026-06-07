import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


@router.get("/stats")
def team_overview_stats(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_team_overview_stats(conn))


@router.get("/rebounding")
def team_rebounding_stats(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_team_rebounding_stats(conn))


@router.get("/shot-chart")
def shot_chart_overall(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_shot_chart_overall(conn))


@router.get("/shot-chart/by-quarter")
def shot_chart_by_quarter(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_shot_chart_by_quarter(conn))
