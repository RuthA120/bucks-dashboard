"""
This script is responsible for loading in the data from the
game file and inserting the data into their corresponding
tables.
"""

import csv
import json

def load_data(conn, csv_file):
    cursor = conn.cursor()
    load_player_game_stats(conn, 'data/mil-cha-game-bball-reference.csv')
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            teams = json.loads(row["teams"])
            players = json.loads(row["players"])
            chance_attr = json.loads(row["chanceAttr"])
            clocks = json.loads(row["clocks"])

            shot_info = (
                json.loads(row["chanceShotInfo"])
                if row["chanceShotInfo"]
                else None
            )

            scoring = (
                json.loads(row["scoring"])
                if row["scoring"]
                else None
            )

            drive_info = (
                json.loads(row["driveInfo"])
                if row["driveInfo"]
                else None
            )

            pick_info = (
                json.loads(row["pickInfo"])
                if row["pickInfo"]
                else None
            )

            reb_info = (
                json.loads(row["rebInfo"])
                if row["rebInfo"]
                else None
            )

            lineups = (
                json.loads(row["lineups"])
                if row["lineups"]
                else None
            )

            xid_chance = row["xid_chance"]

            insert_players(cursor, players)
            insert_chance(
                cursor, xid_chance, teams, players,
                chance_attr, scoring, clocks
            )

            if shot_info:
                insert_shots(cursor, xid_chance, shot_info)

            if lineups:
                insert_lineups(cursor, xid_chance, lineups)
                update_lineup_key(cursor, xid_chance, lineups, teams)

            if drive_info:
                insert_drive(cursor, xid_chance, drive_info)

            if pick_info:
                insert_pick(cursor, xid_chance, pick_info)

            if reb_info:
                insert_rebound(cursor, xid_chance, reb_info)


    conn.commit()
    cursor.close()

def insert_players(cursor, players_json):
    player_roles = ["bringUpBhr", "chanceUser", "chanceCreator"]

    for role in player_roles:
        player = players_json.get(role)
        if not player:
            continue

        cursor.execute("""
            INSERT OR IGNORE INTO players
            VALUES (?, ?, ?, ?)
        """, (
            player["pid_s2"],
            player["pid_nba"],
            player["nameFirst_s2"],
            player["nameLast_s2"]
        ))

def insert_chance(
    cursor, xid_chance, teams, players,
    chance_attr, scoring, clocks
):
    cursor.execute("""
        INSERT OR IGNORE INTO chances (
            xid_chance,
            period,
            offense_team,
            defense_team,
            chance_user_id,
            chance_creator_id,
            outcome,
            pts_scored,
            expected_pts,
            start_game_clock,
            end_game_clock,
            category,
            transition,
            ball_in_paint,
            zone,
            reversals,
            after_timeout
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        xid_chance,
        clocks["period"],
        teams["teamOffense"]["teamInfo"]["teamAbbrev_s2"],
        teams["teamDefense"]["teamInfo"]["teamAbbrev_s2"],
        (players.get("chanceUser") or {}).get("pid_s2"),
        (players.get("chanceCreator") or {}).get("pid_s2"),
        chance_attr["outcome"],
        scoring["ptsScored"] if scoring else 0,
        scoring["xPts"] if scoring else None,
        clocks["startGameClock"],
        clocks["endGameClock"],
        chance_attr.get("category"),
        chance_attr.get("transition", 0),
        chance_attr.get("ballInPaint", 0),
        chance_attr.get("zone", 0),
        chance_attr.get("reversals", 0),
        chance_attr.get("afterTimeout", 0)
    ))

def insert_shots(cursor, xid_chance, shot_info):
    for shot in shot_info.get("shotList", []):
        cursor.execute("""
            INSERT OR IGNORE INTO shots (
                xid_shot,
                xid_chance,
                shooter_id,
                passer_id,
                defender_id,
                made,
                is_three,
                qsq,
                qsp,
                region,
                x_loc,
                y_loc
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            shot["xid_shot"],
            xid_chance,
            (shot.get("shooter") or {}).get("pid_s2"),
            (shot.get("passer") or {}).get("pid_s2"),
            (shot.get("closestDef") or {}).get("pid_s2"),
            bool(shot.get("fg", 0)),
            bool(shot.get("fg3", 0)),
            shot.get("qSQ"),
            shot.get("qSP"),
            shot.get("region"),
            shot.get("location", [None, None])[0],
            shot.get("location", [None, None])[1]
        ))

def insert_lineups(cursor, xid_chance, lineups):
    on_court = lineups.get("onCourt", {})
    for player in on_court.get("lineupOff", []):
        cursor.execute("""
            INSERT OR IGNORE INTO lineups (
                xid_chance, pid_s2, team_role, lineup_position
            )
            VALUES (?, ?, ?, ?)
        """, (
            xid_chance,
            player["playerInfo"]["pid_s2"],
            "offense",
            player["idx"]
        ))

    for player in on_court.get("lineupDef", []):
        cursor.execute("""
            INSERT OR IGNORE INTO lineups (
                xid_chance, pid_s2, team_role, lineup_position
            )
            VALUES (?, ?, ?, ?)
        """, (
            xid_chance,
            player["playerInfo"]["pid_s2"],
            "defense",
            player["idx"]
        ))

def insert_drive(cursor, xid_chance, drive_info):
    cursor.execute("""
        INSERT OR IGNORE INTO drives (
            xid_chance,
            actions,
            direct_chance,
            pts_scored,
            blowby_opportunities,
            blowbys
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        xid_chance,
        drive_info.get("actions", 0),
        drive_info.get("directChance", 0),
        drive_info.get("ptsScored", 0),
        drive_info.get("blowbyOpp", 0),
        drive_info.get("blowby", 0)
    ))

def insert_pick(cursor, xid_chance, pick_info):
    cursor.execute("""
        INSERT OR IGNORE INTO pick_actions (
            xid_chance,
            actions,
            pts_scored,
            double_team,
            roll,
            pop,
            def_over,
            def_under,
            def_switch
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        xid_chance,
        pick_info.get("actions", 0),
        pick_info.get("ptsScored", 0),
        pick_info.get("double", 0),
        pick_info.get("roll", 0),
        pick_info.get("pop", 0),
        pick_info.get("defOver", 0),
        pick_info.get("defUnder", 0),
        pick_info.get("defSwitch", 0)
    ))

def insert_rebound(cursor, xid_chance, reb_info):
    cursor.execute("""
        INSERT OR IGNORE INTO rebound_actions (
            xid_chance,
            rebound_opportunities,
            defensive_rebounds,
            offensive_rebounds,
            boxout_opportunities,
            boxout_successes,
            boxout_failures,
            boxout_missed,
            rear_boxouts
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        xid_chance,
        reb_info.get("rebOpp", 0),
        reb_info.get("rebDef", 0),
        reb_info.get("rebOff", 0),
        reb_info.get("boxoutOpp", 0),
        reb_info.get("boxoutSuccess", 0),
        reb_info.get("boxoutFailed", 0),
        reb_info.get("boxoutMissed", 0),
        reb_info.get("boxoutRear", 0)
    ))

def build_lineup_key(lineups_json, team_role):
    on_court = lineups_json.get("onCourt", {})
    key = "lineupOff" if team_role == "offense" else "lineupDef"
    players = on_court.get(key, [])
    ids = sorted(p["playerInfo"]["pid_s2"] for p in players)
    return "|".join(ids)


def update_lineup_key(cursor, xid_chance, lineups_json, teams):
    offense_team = teams["teamOffense"]["teamInfo"]["teamAbbrev_s2"]

    if offense_team == "MIL":
        mil_offense_key = build_lineup_key(lineups_json, "offense")
        mil_defense_key = None
    else:
        mil_offense_key = None
        mil_defense_key = build_lineup_key(lineups_json, "defense")

    cursor.execute("""
        UPDATE chances
        SET mil_offense_lineup_key = ?,
            mil_defense_lineup_key = ?
        WHERE xid_chance = ?
    """, (mil_offense_key, mil_defense_key, xid_chance))


def load_player_game_stats(conn, csv_file):
    """
    Loads the separate player box score CSV containing
    FT, rebounds, assists, steals, blocks, etc.
    Call this after load_data() with the box score CSV path.
    """
    cursor = conn.cursor()
    with open(csv_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT OR REPLACE INTO player_game_stats (
                    player_name,
                    team,
                    ft,
                    fta,
                    ft_pct,
                    orb,
                    drb,
                    trb,
                    ast,
                    stl,
                    blk,
                    pf,
                    plus_minus
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row["Name"].strip(),
                row["TEAM"].strip(),
                int(row["FT"] or 0),
                int(row["FTA"] or 0),
                float(row["FT%"] or 0),
                int(row["ORB"] or 0),
                int(row["DRB"] or 0),
                int(row["TRB"] or 0),
                int(row["AST"] or 0),
                int(row["STL"] or 0),
                int(row["BLK"] or 0),
                int(row["PF"] or 0),
                int(row["+/-"] or 0)
            ))
    conn.commit()
    cursor.close()