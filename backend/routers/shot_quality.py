import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


@router.get("/overall")
def shot_quality_overall(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_shot_quality_by_team(conn))


@router.get("/by-quarter")
def shot_quality_by_quarter(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_shot_quality_by_quarter(conn))
