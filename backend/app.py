import sqlite3
from data.create_tables import create_tables
from data.load_data import load_data
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import overview, players, drives, pick_and_roll, shot_quality

app = FastAPI(title="MIL vs CHA Game Report 01/02/26", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("data/mil_cha_game.db")
create_tables(conn)
load_data(conn, "data/mil-cha-1-22-26.csv")

app.include_router(overview.router,      prefix="/overview",      tags=["Overview"])
app.include_router(players.router,       prefix="/players",       tags=["Players"])
app.include_router(drives.router,        prefix="/drives",        tags=["Drives"])
app.include_router(pick_and_roll.router, prefix="/pick-and-roll", tags=["Pick & Roll / Pop"])
app.include_router(shot_quality.router,  prefix="/shot-quality",  tags=["Shot Quality"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}