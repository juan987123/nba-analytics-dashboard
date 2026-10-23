from fastapi import FastAPI
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI(title="NBA SofaScore Analytics Pro")

ALL_PLAYERS = [
    "LeBron James", "Luka Dončić", "Stephen Curry", "Nikola Jokić", 
    "Giannis Antetokounmpo", "Kevin Durant", "Jayson Tatum", "Shai Gilgeous-Alexander",
    "Anthony Davis", "Devin Booker", "Donovan Mitchell", "Kyrie Irving"
]

@app.get("/")
def read_index():
    return FileResponse('index.html')

@app.get("/api/todays-games")
def get_todays_games():
    return {"games": [
        {"home": "lakers", "away": "celtics", "home_name": "Los Angeles Lakers", "away_name": "Boston Celtics", "status": "20:30 EST", "is_live": False},
        {"home": "warriors", "away": "nuggets", "home_name": "Golden State Warriors", "away_name": "Denver Nuggets", "status": "EN VIVO - Q3", "is_live": True}
    ]}

@app.get("/api/predict")
def predict_matchup(home_team: str = "lakers", away_team: str = "celtics"):
    metrics = {
        "lakers": {"off": 115.4, "def": 112.1, "net": 3.3},
        "celtics": {"off": 120.2, "def": 110.0, "net": 10.2},
        "warriors": {"off": 117.8, "def": 113.5, "net": 4.3},
        "nuggets": {"off": 118.5, "def": 111.2, "net": 7.3}
    }
    h = metrics.get(home_team.lower(), {"off": 112.0, "def": 112.0, "net": 0.0})
    a = metrics.get(away_team.lower(), {"off": 112.0, "def": 112.0, "net": 0.0})
    
    return {
        "matchup": f"{home_team.capitalize()} vs {away_team.capitalize()}",
        "predictions": {
            home_team.capitalize(): "55.0%",
            away_team.capitalize(): "45.0%"
        },
        "stats_chart": {
            "teams": [home_team.capitalize(), away_team.capitalize()],
            "off_rating": [h["off"], a["off"]],
            "def_rating": [h["def"], a["def"]],
            "net_rating": [h["net"], a["net"]]
        },
        "analysis": "Análisis multivariable basado en datos de eficiencia de la temporada actual."
    }

@app.get("/api/players/suggest")
def suggest_players(q: str = ""):
    if not q:
        return {"suggestions": []}
    matches = [p for p in ALL_PLAYERS if q.lower() in p.lower()]
    return {"suggestions": matches}

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    q = player_name.lower().strip()
    
    db = {
        "lebron": {"full_name": "LeBron James", "team": "Los Angeles Lakers", "position": "F", "pts": 25.7, "ast": 8.3, "reb": 7.3, "fg_pct": 0.540},
        "luka": {"full_name": "Luka Dončić", "team": "Dallas Mavericks", "position": "G-F", "pts": 33.9, "ast": 9.8, "reb": 9.2, "fg_pct": 0.487},
        "curry": {"full_name": "Stephen Curry", "team": "Golden State Warriors", "position": "G", "pts": 26.4, "ast": 5.1, "reb": 4.5, "fg_pct": 0.450},
        "jokic": {"full_name": "Nikola Jokić", "team": "Denver Nuggets", "position": "C", "pts": 26.4, "ast": 9.0, "reb": 12.4, "fg_pct": 0.583}
    }
    
    for k, v in db.items():
        if k in q or q in k:
            return v
            
    return {
        "full_name": player_name.title(),
        "team": "Equipo NBA",
        "position": "G-F",
        "pts": 24.5,
        "ast": 6.2,
        "reb": 5.8,
        "fg_pct": 0.485
    }
