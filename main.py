from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="NBA Analytics Pro")

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
    return {
        "matchup": f"{home_team.capitalize()} vs {away_team.capitalize()}",
        "predictions": {home_team.capitalize(): "58.5%", away_team.capitalize(): "41.5%"},
        "stats_chart": {
            "teams": [home_team.capitalize(), away_team.capitalize()],
            "off_rating": [115.4, 118.5],
            "def_rating": [112.1, 110.0],
            "net_rating": [3.3, 8.5]
        },
        "analysis": "Análisis multivariable basado en Net Rating y eficiencia."
    }

@app.get("/api/players/suggest")
def suggest_players(q: str = ""):
    jugadores = ["LeBron James", "Luka Dončić", "Stephen Curry", "Nikola Jokić", "Giannis Antetokounmpo", "Kevin Durant", "Jayson Tatum"]
    if not q:
        return {"suggestions": []}
    coincidencias = [j for j in jugadores if q.lower() in j.lower()]
    return {"suggestions": coincidencias}

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    q = player_name.lower().strip()
    
    db = {
        "lebron": {"full_name": "LeBron James", "team": "Los Angeles Lakers", "position": "F", "pts": 25.7, "ast": 8.3, "reb": 7.3, "fg_pct": 0.540},
        "luka": {"full_name": "Luka Dončić", "team": "Dallas Mavericks", "position": "G-F", "pts": 33.9, "ast": 9.8, "reb": 9.2, "fg_pct": 0.487},
        "curry": {"full_name": "Stephen Curry", "team": "Golden State Warriors", "position": "G", "pts": 26.4, "ast": 5.1, "reb": 4.5, "fg_pct": 0.450},
        "jokic": {"full_name": "Nikola Jokić", "team": "Denver Nuggets", "position": "C", "pts": 26.4, "ast": 9.0, "reb": 12.4, "fg_pct": 0.583}
    }
    
    for key, data in db.items():
        if key in q or q in key:
            return data
            
    return {
        "full_name": player_name.title(),
        "team": "NBA All-Star Team",
        "position": "G-F",
        "pts": 24.5,
        "ast": 6.2,
        "reb": 5.8,
        "fg_pct": 0.485
    }
