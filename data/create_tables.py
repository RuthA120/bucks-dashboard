"""
This file is responsible for the schema creation of the program's tables.

Tables:
- games
- teams
- players
- chances
- shots
"""

def create_tables(conn):
    cursor = conn.cursor()

    # games table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            gid_s2 VARCHAR(50) PRIMARY KEY,
            gid_nba VARCHAR(20),
            season INTEGER,
            season_type VARCHAR(50),
            game_date DATE,
            home_team_id VARCHAR(50),
            away_team_id VARCHAR(50)
        )
    """)

    # teams table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS teams (
            tid_s2 VARCHAR(50) PRIMARY KEY,
            tid_nba BIGINT,
            team_name VARCHAR(100),
            team_abbrev VARCHAR(10)
        )
    """)

    # players table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            pid_s2 VARCHAR(50) PRIMARY KEY,
            pid_nba BIGINT,
            first_name VARCHAR(100),
            last_name VARCHAR(100)
        )
    """)

    # chances table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chances (
            xid_chance VARCHAR(50) PRIMARY KEY,
            gid_s2 VARCHAR(50),

            period INTEGER,

            offense_team_id VARCHAR(50),
            defense_team_id VARCHAR(50),

            chance_user_id VARCHAR(50),
            chance_creator_id VARCHAR(50),

            outcome VARCHAR(20),

            pts_scored INTEGER,
            expected_pts FLOAT,

            start_game_clock FLOAT,
            end_game_clock FLOAT,

            FOREIGN KEY (gid_s2) REFERENCES games(gid_s2)
        )
    """)

    # shots table schema
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shots (
            xid_shot VARCHAR(50) PRIMARY KEY,
            xid_chance VARCHAR(50),

            shooter_id VARCHAR(50),
            passer_id VARCHAR(50),
            defender_id VARCHAR(50),

            made BOOLEAN,
            is_three BOOLEAN,

            qsq FLOAT,
            qsp FLOAT,

            region VARCHAR(50),

            x_loc FLOAT,
            y_loc FLOAT,

            FOREIGN KEY (xid_chance) REFERENCES chances(xid_chance)
        )
    """)

    conn.commit()
    cursor.close()