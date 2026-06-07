import sqlite3
from fastapi import APIRouter, Depends
from data.database import get_db
from data import insights

router = APIRouter()


def _rows_to_list(rows) -> list[dict]:
    return [dict(row) for row in rows]


def _top(lst: list[dict], key: str):
    filtered = [p for p in lst if p.get(key) is not None and p[key] != 0]
    return max(filtered, key=lambda p: p[key]) if filtered else None


@router.get("/scoring")
def player_scoring_stats(conn: sqlite3.Connection = Depends(get_db)):
    return _rows_to_list(insights.get_player_scoring_stats(conn))


@router.get("/leaders")
def stat_leaders(conn: sqlite3.Connection = Depends(get_db)):
    scoring = _rows_to_list(insights.get_points_leader(conn))
    rebounding = _rows_to_list(insights.get_rebounds_leader(conn))
    assists = _rows_to_list(insights.get_assists_leader(conn))
    steals_blocks = _rows_to_list(insights.get_steals_blocks_leader(conn))

    result = {}
    for team in ('MIL', 'CHA'):
        s  = [r for r in scoring       if r['team'] == team]
        rb = [r for r in rebounding    if r['team'] == team]
        a  = [r for r in assists       if r['team'] == team]
        sb = [r for r in steals_blocks if r['team'] == team]

        result[team] = {
            'scoring_leader': _top(s,  'pts'),
            'rebounding_leader': _top(rb, 'trb'),
            'assist_leader': _top(a,  'ast'),
            'steals_blocks_leader': _top(sb, 'stocks'),
        }

    return result