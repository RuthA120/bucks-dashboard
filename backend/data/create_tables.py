"""
This file is responsible for creating the database schema.

Tables:
- players
- chances
- shots
- lineups
- drives
- isolation_actions
- pick_actions
- pass_actions
- rebound_actions
- crash_rebounds
"""


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS shots")
    cursor.execute("DROP TABLE IF EXISTS lineups")
    cursor.execute("DROP TABLE IF EXISTS drives")
    cursor.execute("DROP TABLE IF EXISTS isolation_actions")
    cursor.execute("DROP TABLE IF EXISTS pick_actions")
    cursor.execute("DROP TABLE IF EXISTS pass_actions")
    cursor.execute("DROP TABLE IF EXISTS rebound_actions")
    cursor.execute("DROP TABLE IF EXISTS crash_rebounds")
    cursor.execute("DROP TABLE IF EXISTS chances")
    cursor.execute("DROP TABLE IF EXISTS players")

    cursor.execute("""
        CREATE TABLE players (
            pid_s2 TEXT PRIMARY KEY,
            pid_nba INTEGER,
            first_name TEXT,
            last_name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE chances (
            xid_chance TEXT PRIMARY KEY,

            period INTEGER,

            offense_team TEXT,
            defense_team TEXT,

            chance_user_id TEXT,
            chance_creator_id TEXT,

            outcome TEXT,

            pts_scored INTEGER,
            expected_pts REAL,

            start_game_clock REAL,
            end_game_clock REAL,

            category TEXT,
            transition INTEGER,
            ball_in_paint INTEGER,
            zone INTEGER,
            reversals INTEGER,
            after_timeout INTEGER
        )
    """)

    cursor.execute("""
        CREATE TABLE shots (
            xid_shot TEXT PRIMARY KEY,
            xid_chance TEXT,

            shooter_id TEXT,
            passer_id TEXT,
            defender_id TEXT,

            made INTEGER,
            is_three INTEGER,

            qsq REAL,
            qsp REAL,

            region TEXT,

            x_loc REAL,
            y_loc REAL,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE lineups (
            xid_chance TEXT,
            pid_s2 TEXT,
            team_role TEXT,
            lineup_position INTEGER,

            PRIMARY KEY (xid_chance, pid_s2),

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance),

            FOREIGN KEY (pid_s2)
                REFERENCES players(pid_s2)
        )
    """)

    # -------------------------
    # Drives
    # -------------------------

    cursor.execute("""
        CREATE TABLE drives (
            xid_chance TEXT PRIMARY KEY,

            actions INTEGER,
            direct_chance INTEGER,
            pts_scored INTEGER,

            blowby_opportunities INTEGER,
            blowbys INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE isolation_actions (
            xid_chance TEXT PRIMARY KEY,

            actions INTEGER,
            direct_chance INTEGER,
            pts_scored INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE pick_actions (
            xid_chance TEXT PRIMARY KEY,

            actions INTEGER,
            direct_chance INTEGER,
            pts_scored INTEGER,

            double_team INTEGER,

            roll INTEGER,
            pop INTEGER,

            def_over INTEGER,
            def_under INTEGER,
            def_switch INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE pass_actions (
            xid_chance TEXT PRIMARY KEY,

            passes INTEGER,
            completed INTEGER,

            assist_opportunities INTEGER,
            secondary_assists INTEGER,

            turnovers INTEGER,
            deflections INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE rebound_actions (
            xid_chance TEXT PRIMARY KEY,

            rebound_opportunities INTEGER,

            defensive_rebounds INTEGER,
            offensive_rebounds INTEGER,

            boxout_opportunities INTEGER,
            boxout_successes INTEGER,
            boxout_failures INTEGER,
            boxout_missed INTEGER,
            rear_boxouts INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    cursor.execute("""
        CREATE TABLE crash_rebounds (
            xid_chance TEXT PRIMARY KEY,

            crashed INTEGER,
            rebounded INTEGER,

            FOREIGN KEY (xid_chance)
                REFERENCES chances(xid_chance)
        )
    """)

    conn.commit()
    cursor.close()