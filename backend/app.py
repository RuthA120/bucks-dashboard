import sqlite3
from data.create_tables import create_tables
from data.load_data import load_data

conn = sqlite3.connect("data/mil_cha_game.db")

create_tables(conn)
load_data(conn, "data/mil-cha-1-22-26.csv")

conn.close()