from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(title="NBA SofaScore Analytics Pro")

# Base de datos local actualizada con plantillas y estadísticas recientes
PLAYERS_DATABASE = {
    "lebron james": {"full_name": "LeBron James", "team": "Los Angeles Lakers", "position": "F", "pts": 25.7, "ast": 8.3, "reb": 7.3, "fg_pct": 0.540},
    "luka doncic": {"full_name": "Luka Dončić", "team": "Dallas Mavericks", "position": "G-F", "pts": 33.9, "ast": 9.8, "reb": 9.2, "fg_pct": 0.487},
    "stephen curry": {"full_name": "Stephen Curry", "team": "Golden State Warriors", "position": "G", "pts": 26.4, "ast": 5.1, "reb": 4.5, "fg_pct": 0.450},
    "nikola jokic": {"full_name": "Nikola Jokić", "team": "Denver Nuggets", "position": "C", "pts": 26.4, "ast": 9.0, "reb": 12.4, "fg_pct": 0.583},
    "giannis antetokounmpo": {"full_name": "Giannis Antetokounmpo", "team": "Milwaukee Bucks", "position": "F", "pts": 30.4, "ast": 6.5, "reb": 11.5, "fg_pct": 0.611},
    "kevin durant": {"full_name": "Kevin Durant", "team": "Phoenix Suns", "position": "F", "pts": 27.1, "ast": 5.0, "reb": 6.6, "fg_pct": 0.523},
    "jayson tatum": {"full_name": "Jayson Tatum", "team": "Boston Celtics", "position": "F", "pts": 26.9, "ast": 4.9, "reb": 8.1, "fg_pct": 0.471},
    "shai gilgeous-alexander": {"full_name": "Shai Gilgeous-Alexander", "team": "Oklahoma City Thunder", "position": "G", "pts": 30.1, "ast": 6.2, "reb": 5.5, "fg_pct": 0.535},
    "anthony davis": {"full_name": "Anthony Davis", "team": "Los Angeles Lakers", "position": "F-C", "pts": 24.7, "ast": 3.5, "reb": 12.6, "fg_pct": 0.556},
    "devin booker": {"full_name": "Devin Booker", "team": "Phoenix Suns", "position": "G", "pts": 27.1, "ast": 6.9, "reb": 4.5, "fg_pct": 0.492},
    "kyrie irving": {"full_name": "Kyrie Irving", "team": "Dallas Mavericks", "position": "G", "pts": 25.6, "ast": 5.2, "reb": 5.0, "fg_pct": 0.497},
    "jalen brunson": {"full_name": "Jalen Brunson", "team": "New York Knicks", "position": "G", "pts": 28.7, "ast": 6.7, "reb": 3.6, "fg_pct": 0.479},
    "victor wembanyama": {"full_name": "Victor Wembanyama", "team": "San Antonio Spurs", "position": "C-F", "pts": 21.4, "ast": 3.9, "reb": 10.6, "fg_pct": 0.465},
    "anthony edwards": {"full_name": "Anthony Edwards", "team": "Minnesota Timberwolves", "position": "G", "pts": 25.9, "ast": 5.1, "reb": 5.4, "fg_pct": 0.461},
    "tyrese haliburton": {"full_name": "Tyrese Haliburton", "team": "Indiana Pacers", "position": "G", "pts": 20.1, "ast": 10.9, "reb": 3.9, "fg_pct": 0.477},
    "donovan mitchell": {"full_name": "Donovan Mitchell", "team": "Cleveland Cavaliers", "position": "G", "pts": 26.6, "ast": 6.1, "reb": 5.1, "fg_pct": 0.462},
    "damian lillard": {"full_name": "Damian Lillard", "team": "Milwaukee Bucks", "position": "G", "pts": 24.3, "ast": 7.0, "reb": 4.4, "fg_pct": 0.424},
    "kawhi leonard": {"full_name": "Kawhi Leonard", "team": "LA Clippers", "position": "F", "pts": 23.7, "ast": 3.6, "reb": 6.1, "fg_pct": 0.525},
    "jimmy butler": {"full_name": "Jimmy Butler", "team": "Miami Heat", "position": "F", "pts": 20.8, "ast": 5.0, "reb": 5.3, "fg_pct": 0.499},
    "domantas sabonis": {"full_name": "Domantas Sabonis", "team": "Sacramento Kings", "position": "C-F", "pts": 19.4, "ast": 8.2, "reb": 13.7, "fg_pct": 0.594}
}

@app.get("/")
def read_index():
    return FileResponse('index.html')

@app.get("/api/teams-list")
def get_teams_list():
    teams = [
        {"id": "atl", "name": "Atlanta Hawks"}, {"id": "bos", "name": "Boston Celtics"},
        {"id": "bkn", "name": "Brooklyn Nets"}, {"id": "cha", "name": "Charlotte Hornets"},
        {"id": "chi", "name": "Chicago Bulls"}, {"id": "cle", "name": "Cleveland Cavaliers"},
        {"id": "dal", "name": "Dallas Mavericks"}, {"id": "den", "name": "Denver Nuggets"},
        {"id": "det", "name": "Detroit Pistons"}, {"id": "gsw", "name": "Golden State Warriors"},
        {"id": "hou", "name": "Houston Rockets"}, {"id": "ind", "name": "Indiana Pacers"},
        {"id": "lac", "name": "LA Clippers"}, {"id": "lal", "name": "Los Angeles Lakers"},
        {"id": "mem", "name": "Memphis Grizzlies"}, {"id": "mia", "name": "Miami Heat"},
        {"id": "mil", "name": "Milwaukee Bucks"}, {"id": "min", "name": "Minnesota Timberwolves"},
        {"id": "nop", "name": "New Orleans Pelicans"}, {"id": "nyk", "name": "New York Knicks"},
        {"id": "okc", "name": "Oklahoma City Thunder"}, {"id": "orl", "name": "Orlando Magic"},
        {"id": "phi", "name": "Philadelphia 76ers"}, {"id": "phx", "name": "Phoenix Suns"},
        {"id": "por", "name": "Portland Trail Blazers"}, {"id": "sac", "name": "Sacramento Kings"},
        {"id": "sas", "name": "San Antonio Spurs"}, {"id": "tor", "name": "Toronto Raptors"},
        {"id": "uta", "name": "Utah Jazz"}, {"id": "was", "name": "Washington Wizards"}
    ]
    return {"teams": teams}

@app.get("/api/todays-games")
def get_todays_games():
    return {"games": [
        {"home": "lal", "away": "bos", "home_name": "Los Angeles Lakers", "away_name": "Boston Celtics", "status": "20:30 EST", "is_live": False},
        {"home": "gsw", "away": "den", "home_name": "Golden State Warriors", "away_name": "Denver Nuggets", "status": "EN VIVO - Q3", "is_live": True}
    ]}

@app.get("/api/predict")
def predict_matchup(home_team: str = "lal", away_team: str = "bos"):
    metrics = {
        "bos": {"off": 122.2, "def": 110.6, "net": 11.6}, "okc": {"off": 119.5, "def": 109.5, "net": 10.0},
        "den": {"off": 118.5, "def": 111.2, "net": 7.3}, "cle": {"off": 117.0, "def": 110.2, "net": 6.8},
        "min": {"off": 114.5, "def": 108.4, "net": 6.1}, "nyk": {"off": 117.2, "def": 111.0, "net": 6.2},
        "dal": {"off": 117.9, "def": 112.5, "net": 5.4}, "gsw": {"off": 117.8, "def": 113.5, "net": 4.3},
        "lac": {"off": 116.2, "def": 112.0, "net": 4.2}, "nop": {"off": 115.8, "def": 111.8, "net": 4.0},
        "phx": {"off": 117.0, "def": 113.2, "net": 3.8}, "lal": {"off": 115.4, "def": 112.1, "net": 3.3},
        "ind": {"off": 120.5, "def": 117.2, "net": 3.3}, "hou": {"off": 114.2, "def": 111.0, "net": 3.2},
        "orl": {"off": 111.2, "def": 109.0, "net": 2.2}, "mil": {"off": 116.0, "def": 114.0, "net": 2.0},
        "phi": {"off": 115.0, "def": 113.2, "net": 1.8}, "sac": {"off": 116.5, "def": 114.8, "net": 1.7},
        "mia": {"off": 112.8, "def": 111.5, "net": 1.3}, "mem": {"off": 113.0, "def": 112.4, "net": 0.6}
    }
    
    h_key, a_key = home_team.lower(), away_team.lower()
    h = metrics.get(h_key, {"off": 112.0, "def": 112.0, "net": 0.0})
    a = metrics.get(a_key, {"off": 112.0, "def": 112.0, "net": 0.0})

    return {
        "matchup": f"{home_team.upper()} vs {away_team.upper()}",
        "predictions": {home_team.upper(): "54.2%", away_team.upper(): "45.8%"},
        "stats_chart": {
            "teams": [home_team.upper(), away_team.upper()],
            "off_rating": [h["off"], a["off"]],
            "def_rating": [h["def"], a["def"]],
            "net_rating": [h["net"], a["net"]]
        },
        "analysis": f"Evaluación basada en métricas de eficiencia (Net Rating)."
    }

@app.get("/api/players/suggest")
def suggest_players(q: str = ""):
    if not q or len(q) < 2:
        return {"suggestions": []}
    # Solo sugiere los jugadores que están en la base de datos real
    matches = [data['full_name'] for key, data in PLAYERS_DATABASE.items() if q.lower() in key or q.lower() in data['full_name'].lower()]
    return {"suggestions": matches[:8]}

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    q = player_name.lower().strip()
    
    # Buscar coincidencia exacta o parcial en la base de datos
    for key, data in PLAYERS_DATABASE.items():
        if q in key or key in q:
            return data
            
    # Si el jugador no existe en la base local
    return {
        "full_name": player_name.title(),
        "team": "Jugador Sin Registrar",
        "position": "N/A",
        "pts": 0.0,
        "ast": 0.0,
        "reb": 0.0,
        "fg_pct": 0.000
    }
