# MIL vs CHA Game Report Dashboard
## By: Ruth Assefa
A game report dashboard for the Milwaukee Bucks vs Charlotte Hornets game (January 2, 2026). Built with a FastAPI backend and React frontend.

---
## Prerequisites
Make sure you have the following installed:
- **Python 3.10+**
- **Node.js 18+** and **npm**
---

## Setup
### 1. Clone the repository

```bash
git clone https://github.com/RuthA120/bucks-dashboard.git
cd bucks-dashboard
```
---

### 2. Backend

```bash
cd backend
```

Create and activate a virtual environment:
```bash
# Mac / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Start the server:
```bash
uvicorn app:app --reload
```
The API will be running at **http://localhost:8000**.

> The database is created and loaded automatically on startup (no need to set it up!)

---

### 3. Frontend

Open a new terminal tab:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be running at **http://localhost:5173**.

---

## Project Structure

```
bucks-dashboard/
├── backend/
│   ├── app.py                        # FastAPI entry point
│   ├── requirements.txt
│   ├── routers/                      # API route handlers
│   │   ├── overview.py
│   │   ├── players.py
│   │   ├── drives.py
│   │   ├── pick_and_roll.py
│   │   └── shot_quality.py
│   └── data/
│       ├── create_tables.py          # Database schema
│       ├── load_data.py              # CSV file loads
│       ├── insights.py               # All analytics queries
│       ├── database.py               # DB connection helper
│       └── mil-cha-1-22-26.csv       # Raw game data
└── frontend/
    ├── src/
    │   ├── App.jsx                   # Root component + nav
    │   └── components/               # One component per tab
    └── package.json
```

---

## Usage

With both servers running, open **http://localhost:5173** in your browser. 
Here are the navigation tabs that you can explore:
- **Overview** — box score and shot chart
- **Players** — individual scoring and leaders
- **Drives** — drive creation and defensive breakdowns
- **Pick & Roll** — roll vs pop efficiency and defensive coverages
- **Shot Quality** — qSQ/qSP trends by quarter and shooter


## Design Choices
- **Table Creation**: I thought it would be best to store the game data into a database because querying this data with pandas or using Python on its own would be a complex process for filtering and aggregating the data since we would have to re-parse the JSON. Storing the data into SQL tables makes data insertion easy, and
it makes the querying process easier when we have to integrate it to the backend.

- **Schema Design**: Chances table is the main table since it stores every offensive opportunity and outcome and all the other tables can join back to it on the xid_chance attribute. The players table keeps track of players in the game and the player_game_stats table is just a supplementary table to provide box score stats that is difficult or not able to be obtained through the current data. The rest of the tables capture specific moments of the game such as the drives table only containing 'chances' in the game where a drive was recorded.

- **API**: Each router only imports the query functions it needs from the insights.py file which helps keep everything straightforward and understandable.


## Insights
- Refer to the "01_02 Game Report Insights.pdf" file to see the insights game report!
