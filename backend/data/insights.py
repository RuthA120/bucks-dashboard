"""
This script contains all of the analytics that will
appear on the dashboard site. Analytics will include...
- Overview of the game 
- Player Profiles
- Drives
- Pick and Roll/Pop
- Shot Quality
- Lineups
"""

import sqlite3


"""
Overview of the Game
- Looking at standard stats such as PTS, FGA, FGM, 
DREB, OREB, etc. overall and by quarter
- Will also look at shot chart to get a closer look at 
efficiency per region (overall and by quarter)
"""

def get_team_overview_stats(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            offense_team AS team,
            SUM(pts_scored) AS pts,
            SUM(CASE WHEN outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga,
            SUM(CASE WHEN outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm,
            ROUND(
                CAST(SUM(CASE WHEN outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct,
            SUM(CASE WHEN outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga3,
            SUM(CASE WHEN outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS fg3m,
            ROUND(
                CAST(SUM(CASE WHEN outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg3_pct,
            SUM(CASE WHEN outcome IN ('FGM2','FGX2')
                THEN 1 ELSE 0 END) AS fga2,
            SUM(CASE WHEN outcome = 'FGM2'
                THEN 1 ELSE 0 END) AS fg2m,
            ROUND(
                CAST(SUM(CASE WHEN outcome = 'FGM2'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN outcome IN ('FGM2','FGX2')
                THEN 1 ELSE 0 END), 0), 3) AS fg2_pct,
            SUM(CASE WHEN outcome = 'TO'
                THEN 1 ELSE 0 END) AS turnovers
        FROM chances
        WHERE outcome NOT IN ('EPD', 'Out of Bounds')
        GROUP BY offense_team
    """).fetchall()

def get_team_rebounding_stats(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(r.defensive_rebounds) AS def_reb,
            SUM(r.offensive_rebounds) AS off_reb
        FROM rebound_actions r
        JOIN chances c ON c.xid_chance = r.xid_chance
        GROUP BY c.defense_team
        ORDER BY def_reb DESC
    """).fetchall()

def get_shot_chart_overall(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team AS team,
            s.region,
            SUM(CASE
                WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga,
            SUM(CASE
                WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm,
            ROUND(
                CAST(SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct
        FROM shots s
        JOIN chances c ON c.xid_chance = s.xid_chance
        WHERE c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
        GROUP BY c.offense_team, s.region
        ORDER BY c.offense_team
    """).fetchall()

def get_shot_chart_by_quarter(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team AS team,
            c.period,
            s.region,
            SUM(CASE
                WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga,
            SUM(CASE
                WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm,
            ROUND(
                CAST(SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct
        FROM shots s
        JOIN chances c ON c.xid_chance = s.xid_chance
        WHERE c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
        GROUP BY c.offense_team, s.region, c.period
        ORDER BY c.offense_team, c.period
    """).fetchall()


"""
Players Stats
- Looking at standard stats such as FGM, FGA, FG3A, OREB, DREB, etc. for 
individual players
- Both CHA and MIL will be reviewed here
"""
def get_player_scoring_stats(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            p.first_name || ' ' || p.last_name AS player,
            c.offense_team AS team,
            SUM(c.pts_scored) AS pts,

            SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga,
            SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm,
            ROUND(CAST(SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct,
            SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS fg3m,
            ROUND(CAST(SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg3_pct,
            COALESCE(gs.ft, 0)                          AS ft,
            COALESCE(gs.fta, 0)                         AS fta,
            COALESCE(gs.ft_pct, 0)                      AS ft_pct,
            SUM(CASE WHEN c.outcome = 'TO'
                THEN 1 ELSE 0 END) AS turnovers,
            COALESCE(gs.trb, 0)                         AS trb,
            COALESCE(gs.ast, 0)                         AS ast,
            COALESCE(gs.stl, 0)                         AS stl,
            COALESCE(gs.blk, 0)                         AS blk,
            COALESCE(gs.pf, 0)                          AS pf,
            COALESCE(gs.plus_minus, 0)                  AS plus_minus,
            ROUND(AVG(s.qsq), 2)                        AS avg_qsq,
            ROUND(AVG(s.qsp), 2)                        AS avg_qsp,
            ROUND(SUM(c.expected_pts), 3)               AS expected_points
        FROM chances c
        JOIN players p ON p.pid_s2 = c.chance_user_id
        LEFT JOIN shots s
            ON s.xid_chance = c.xid_chance
            AND s.shooter_id = c.chance_user_id
        LEFT JOIN player_game_stats gs
            ON gs.player_name = p.first_name || ' ' || p.last_name
            AND gs.team = c.offense_team
        WHERE c.outcome NOT IN ('EPD', 'Out of Bounds')
        GROUP BY p.pid_s2, c.offense_team
        ORDER BY pts DESC
    """).fetchall()


def get_points_leader(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            p.first_name || ' ' || p.last_name AS player,
            c.offense_team AS team,
            SUM(c.pts_scored) AS pts,
            COALESCE(gs.ft, 0) AS ft,
            COALESCE(gs.fta, 0) AS fta
        FROM chances c
        JOIN players p ON p.pid_s2 = c.chance_user_id
        LEFT JOIN player_game_stats gs
            ON gs.player_name = p.first_name || ' ' || p.last_name
            AND gs.team = c.offense_team
        WHERE c.outcome NOT IN ('EPD', 'Out of Bounds')
        GROUP BY p.pid_s2, c.offense_team
        ORDER BY c.offense_team, pts DESC
    """).fetchall()


def get_assists_leader(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            player_name AS player,
            team,
            ast
        FROM player_game_stats
        WHERE ast IS NOT NULL
        ORDER BY team, ast DESC
    """).fetchall()


def get_rebounds_leader(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            player_name AS player,
            team,
            trb
        FROM player_game_stats
        WHERE trb IS NOT NULL
        ORDER BY team, trb DESC
    """).fetchall()

def get_steals_blocks_leader(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            player_name AS player,
            team,
            stl + blk AS stocks
        FROM player_game_stats
        WHERE stl IS NOT NULL
          AND blk IS NOT NULL
        ORDER BY team, stocks DESC
    """).fetchall()


"""
Drives
- We will look at how effective the Bucks were when making
drives but also defending drive actions from the Hornets
- Looking at MIL's drive actions, we will look through 
various factors ranging from the number of drives were taken,
if blow by opportunities were taken, etc.
- We will look at the number of points CHA managed to score
off of drives and defenders who were beaten off the dribble 
"""
def get_drive_scoring_stats(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team,
            SUM(d.actions) AS total_drives,
            SUM(d.pts_scored) AS drive_pts_scored,
                ROUND(CAST(SUM(d.pts_scored) AS REAL) /
                NULLIF(SUM(d.actions), 0), 3) AS pts_per_drive,
            SUM(CASE
                WHEN d.pts_scored > 0
                THEN d.blowbys
                ELSE 0
            END) AS blowbys_in_scoring_drives,
            SUM(d.blowby_opportunities) AS num_blowby_opportunities,
            ROUND(CAST(
                SUM(CASE
                WHEN d.pts_scored > 0
                THEN d.blowbys
                ELSE 0
                END) AS REAL
            ) / NULLIF(SUM(d.blowbys), 0), 3) AS blowby_success_rate
        FROM drives d
        JOIN chances c ON c.xid_chance = d.xid_chance
        GROUP BY c.offense_team
        ORDER BY drive_pts_scored DESC
    """).fetchall()

def get_drive_finishers(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            p.first_name || ' ' || p.last_name AS player,
            c.offense_team AS team,
            COUNT(DISTINCT d.xid_chance) AS drive_finish_attempts,
            SUM(CASE WHEN c.outcome LIKE 'FGM%'
                THEN 1 ELSE 0 END) AS makes,
            ROUND(CAST(SUM(CASE WHEN c.outcome LIKE 'FGM%'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(COUNT(DISTINCT d.xid_chance), 0), 3) AS finish_rate,
            SUM(d.pts_scored) AS pts_scored
        FROM drives d
        JOIN chances c ON c.xid_chance = d.xid_chance
        JOIN players p ON p.pid_s2 = c.chance_user_id
        WHERE c.offense_team = 'MIL'
          AND d.direct_chance = 1
        GROUP BY p.pid_s2
        ORDER BY pts_scored DESC
    """).fetchall()

def get_defenders_beaten_off_dribble(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            p.first_name || ' ' || p.last_name AS defender,
            c.defense_team AS team,
            SUM(d.blowbys) AS blowbys_allowed,
            SUM(d.blowby_opportunities) AS blowby_opportunities,
            ROUND(CAST(SUM( d.blowbys) AS REAL) /
                NULLIF(SUM( d.blowby_opportunities), 0), 3) AS blowby_rate_allowed
        FROM drives d
        JOIN chances c ON c.xid_chance = d.xid_chance
        JOIN shots s ON s.xid_chance = d.xid_chance
        JOIN players p ON p.pid_s2 = s.defender_id
        WHERE c.defense_team = 'MIL'
        GROUP BY p.pid_s2
        HAVING blowbys_allowed > 1
        ORDER BY blowbys_allowed DESC
    """).fetchall()


"""
Pick n Roll/Pop
- We will look at how effective the Bucks were in their
pick n roll and pick n pop offense
- We will also look at the defensive coverages the Bucks
used against the Hornet's pick n pop and pick n roll
plays.
- We will also look at defense for picks/screens in general
"""

def get_offense_roll_and_pop_stats(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team AS team,
            SUM(pk.roll) AS roll_actions,
            SUM(CASE WHEN pk.roll = 1
                THEN c.pts_scored ELSE 0 END) AS roll_pts,
            ROUND(CAST(SUM(CASE WHEN pk.roll = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.roll), 0), 3) AS pts_per_roll,
            SUM(pk.pop) AS pop_actions,
            SUM(CASE WHEN pk.pop = 1
                THEN c.pts_scored ELSE 0 END) AS pop_pts,
            ROUND(CAST(SUM(CASE WHEN pk.pop = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.pop), 0), 3) AS pts_per_pop
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        GROUP BY c.offense_team
        ORDER BY roll_actions DESC
    """).fetchall()

def get_roll_defensive_coverage(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.def_over) AS over_count,
            SUM(CASE WHEN pk.def_over = 1
                THEN c.pts_scored ELSE 0 END) AS pts_allowed_over,
            ROUND(CAST(SUM(CASE WHEN pk.def_over = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_over), 0), 3) AS pts_per_over,
            SUM(pk.def_under) AS under_count,
            SUM(CASE WHEN pk.def_under = 1
                THEN c.pts_scored ELSE 0 END) AS pts_allowed_under,
            ROUND(CAST(SUM(CASE WHEN pk.def_under = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_under), 0), 3) AS pts_per_under,
            SUM(pk.def_switch) AS switch_count,
            SUM(CASE WHEN pk.def_switch = 1
                THEN c.pts_scored ELSE 0 END)   AS pts_allowed_switch,
                ROUND(CAST(SUM(CASE WHEN pk.def_switch = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_switch), 0), 3) AS pts_per_switch
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        WHERE pk.roll = 1 AND pk.pop = 0
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()


def get_pop_defensive_coverage(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.def_over) AS over_count,
            SUM(CASE WHEN pk.def_over = 1
                THEN c.pts_scored ELSE 0 END)   AS pts_allowed_over,
                ROUND(CAST(SUM(CASE WHEN pk.def_over = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_over), 0), 3) AS pts_per_over,
            SUM(pk.def_under) AS under_count,
            SUM(CASE WHEN pk.def_under = 1
                THEN c.pts_scored ELSE 0 END)   AS pts_allowed_under,
                ROUND(CAST(SUM(CASE WHEN pk.def_under = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_under), 0), 3) AS pts_per_under,
            SUM(pk.def_switch) AS switch_count,
            SUM(CASE WHEN pk.def_switch = 1
                THEN c.pts_scored ELSE 0 END)   AS pts_allowed_switch,
                ROUND(CAST(SUM(CASE WHEN pk.def_switch = 1
                THEN c.pts_scored ELSE 0 END) AS REAL) /
                NULLIF(SUM(pk.def_switch), 0), 3) AS pts_per_switch
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        WHERE pk.pop = 1 AND pk.roll = 0
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()

def get_over_screen_pts_allowed(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.def_over) AS over_count,
            SUM(CASE WHEN pk.def_over = 1
            THEN c.pts_scored ELSE 0 END) AS pts_allowed,
            ROUND(CAST(SUM(CASE WHEN pk.def_over = 1
            THEN c.pts_scored ELSE 0 END) AS REAL) /
            NULLIF(SUM(pk.def_over), 0), 3) AS pts_per_over
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()


def get_under_screen_pts_allowed(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.def_under) AS under_count,
            SUM(CASE WHEN pk.def_under = 1
            THEN c.pts_scored ELSE 0 END) AS pts_allowed,
            ROUND(CAST(SUM(CASE WHEN pk.def_under = 1
            THEN c.pts_scored ELSE 0 END) AS REAL) /
            NULLIF(SUM(pk.def_under), 0), 3) AS pts_per_under
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()

def get_switch_pts_allowed(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.def_switch) AS switch_count,
            SUM(CASE WHEN pk.def_switch = 1
            THEN c.pts_scored ELSE 0 END) AS pts_allowed,
            ROUND(CAST(SUM(CASE WHEN pk.def_switch = 1
            THEN c.pts_scored ELSE 0 END) AS REAL) /
            NULLIF(SUM(pk.def_switch), 0), 3) AS pts_per_switch
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()

def get_double_team_pts_allowed(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.defense_team AS team,
            SUM(pk.double_team) AS double_team_count,
            SUM(CASE WHEN pk.double_team = 1
            THEN c.pts_scored ELSE 0 END) AS pts_allowed,
            ROUND(CAST(SUM(CASE WHEN pk.double_team = 1
            THEN c.pts_scored ELSE 0 END) AS REAL) /
            NULLIF(SUM(pk.double_team), 0),3) AS pts_per_double_team
        FROM pick_actions pk
        JOIN chances c ON c.xid_chance = pk.xid_chance
        GROUP BY c.defense_team
        ORDER BY c.defense_team
    """).fetchall()


"""
Shot Quality
- We will look at both MIL and CHA overall and quarter
field goal percentage, qSQ, and qSP averages.
"""

def get_shot_quality_by_team(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team AS team,
            ROUND(CAST(
                SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL
                ) / NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct,
            ROUND(AVG(s.qsq), 2)                    AS avg_qsq,
            ROUND(AVG(s.qsp), 2)                    AS avg_qsp
        FROM shots s
        JOIN chances c ON c.xid_chance = s.xid_chance
        WHERE c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
        GROUP BY c.offense_team
    """).fetchall()

def get_shot_quality_by_quarter(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.offense_team                          AS team,
            c.period,
            c.offense_team AS team,
            ROUND(CAST(
                SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL
                ) / NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct,
            ROUND(AVG(s.qsq), 2)                    AS avg_qsq,
            ROUND(AVG(s.qsp), 2)                    AS avg_qsp
        FROM shots s
        JOIN chances c ON c.xid_chance = s.xid_chance
        WHERE c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
        GROUP BY c.offense_team, c.period
    """).fetchall()


"""
Lineups
- We will look through some of the lineups ran for offense and defense
and the stats from both sides
"""

def get_mil_lineup_offense(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.mil_offense_lineup_key AS lineup_key,
            COUNT(DISTINCT c.xid_chance) AS chances,
            SUM(c.pts_scored) AS pts_scored,
            ROUND(SUM(c.expected_pts), 3) AS expected_points,
            ROUND(CAST(SUM(c.pts_scored) AS REAL) /
                NULLIF(COUNT(DISTINCT c.xid_chance), 0), 3) AS pts_per_chance,
            SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga,
            SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm,
            ROUND(CAST(SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct,
            SUM(CASE WHEN c.outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga3,
            SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS fg3m,
            ROUND(CAST(SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg3_pct,
            SUM(CASE WHEN c.outcome = 'TO'
                THEN 1 ELSE 0 END) AS turnovers,
            ROUND(AVG(s.qsq), 2) AS avg_qsq,
            ROUND(AVG(s.qsp), 2) AS avg_qsp
        FROM chances c
        LEFT JOIN shots s ON s.xid_chance = c.xid_chance
        WHERE c.offense_team = 'MIL'
          AND c.mil_offense_lineup_key IS NOT NULL
        GROUP BY c.mil_offense_lineup_key
        ORDER BY chances DESC
    """).fetchall()


def get_mil_lineup_defense(conn: sqlite3.Connection):
    return conn.execute("""
        SELECT
            c.mil_defense_lineup_key AS lineup_key,
            COUNT(DISTINCT c.xid_chance) AS chances_defended,
            SUM(c.pts_scored) AS pts_allowed,
            ROUND(SUM(c.expected_pts), 3) AS expected_points_allowed,
            ROUND(CAST(SUM(c.pts_scored) AS REAL) /
                NULLIF(COUNT(DISTINCT c.xid_chance), 0), 3) AS pts_allowed_per_chance,
            SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga_allowed,
            SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS fgm_allowed,
            ROUND(CAST(SUM(CASE WHEN c.outcome IN ('FGM2','FGM3')
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM2','FGX2','FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg_pct_allowed,
            SUM(CASE WHEN c.outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END) AS fga3_allowed,
            SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS fg3m_allowed,
            ROUND(CAST(SUM(CASE WHEN c.outcome = 'FGM3'
                THEN 1 ELSE 0 END) AS REAL) /
                NULLIF(SUM(CASE WHEN c.outcome IN ('FGM3','FGX3')
                THEN 1 ELSE 0 END), 0), 3) AS fg3_pct_allowed,
            SUM(CASE WHEN c.outcome = 'TO'
                THEN 1 ELSE 0 END) AS turnovers_forced,
            ROUND(AVG(s.qsq), 2) AS opp_avg_qsq,
            ROUND(AVG(s.qsp), 2) AS opp_avg_qsp
        FROM chances c
        LEFT JOIN shots s ON s.xid_chance = c.xid_chance
        WHERE c.defense_team = 'MIL'
          AND c.mil_defense_lineup_key IS NOT NULL
        GROUP BY c.mil_defense_lineup_key
        ORDER BY pts_allowed DESC
    """).fetchall()

def get_mil_lineup_player_keys(conn):
    return conn.execute("""
        WITH offense_keys AS (
            SELECT
                c.mil_offense_lineup_key AS lineup_key,
                'offense' AS lineup_type,
                p.first_name || ' ' || p.last_name AS player_name
            FROM chances c
            JOIN lineups l ON l.xid_chance = c.xid_chance
            JOIN players p ON p.pid_s2 = l.pid_s2
            WHERE c.offense_team = 'MIL'
              AND c.mil_offense_lineup_key IS NOT NULL
              AND l.team_role = 'offense'
            GROUP BY c.mil_offense_lineup_key, p.pid_s2
        ),
        defense_keys AS (
            SELECT
                c.mil_defense_lineup_key AS lineup_key,
                'defense' AS lineup_type,
                p.first_name || ' ' || p.last_name AS player_name
            FROM chances c
            JOIN lineups l ON l.xid_chance = c.xid_chance
            JOIN players p ON p.pid_s2 = l.pid_s2
            WHERE c.defense_team = 'MIL'
              AND c.mil_defense_lineup_key IS NOT NULL
              AND l.team_role = 'defense'
            GROUP BY c.mil_defense_lineup_key, p.pid_s2
        )
        SELECT
            lineup_key,
            lineup_type,
            GROUP_CONCAT(player_name, ', ') AS players
        FROM (
            SELECT lineup_key, lineup_type, player_name
            FROM offense_keys
            UNION ALL
            SELECT lineup_key, lineup_type, player_name
            FROM defense_keys
            ORDER BY lineup_key, player_name
        )
        GROUP BY lineup_key, lineup_type
        ORDER BY lineup_type, lineup_key
    """).fetchall()