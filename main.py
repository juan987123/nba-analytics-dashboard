from fastapi import FastAPI
from fastapi.responses import FileResponse
import unicodedata

app = FastAPI(
    title="NBA SofaScore Analytics Pro",
    version="10.0"
)

def normalize_text(text: str) -> str:
    """Normaliza texto eliminando acentos y caracteres especiales para búsquedas exactas."""
    if not text:
        return ""
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return text.lower().replace('č', 'c').replace('ć', 'c').strip()

# FUENTE ÚNICA DE VERDAD: Base de datos centralizada de jugadores activos
# Todos los datos de autocompletado y consulta leen de esta misma estructura.
PLAYERS_DATABASE = [
    {
        "search_key": "giannis antetokounmpo",
        "full_name": "Giannis Antetokounmpo",
        "team": "Milwaukee Bucks",
        "position": "F",
        "pts": 30.8,
        "ast": 6.2,
        "reb": 11.2,
        "fg_pct": 0.605
    },
    {
        "search_key": "luka doncic",
        "full_name": "Luka Dončić",
        "team": "Dallas Mavericks",
        "position": "G-F",
        "pts": 33.9,
        "ast": 9.8,
        "reb": 9.2,
        "fg_pct": 0.487
    },
    {
        "search_key": "lamelo ball",
        "full_name": "LaMelo Ball",
        "team": "Charlotte Hornets",
        "position": "G",
        "pts": 23.9,
        "ast": 8.0,
        "reb": 5.1,
        "fg_pct": 0.433
    },
    {
        "search_key": "lebron james",
        "full_name": "LeBron James",
        "team": "Los Angeles Lakers",
        "position": "F",
        "pts": 25.7,
        "ast": 8.3,
        "reb": 7.3,
        "fg_pct": 0.540
    },
    {
        "search_key": "stephen curry",
        "full_name": "Stephen Curry",
        "team": "Golden State Warriors",
        "position": "G",
        "pts": 26.4,
        "ast": 5.1,
        "reb": 4.5,
        "fg_pct": 0.450
    },
    {
        "search_key": "nikola jokic",
        "full_name": "Nikola Jokić",
        "team": "Denver Nuggets",
        "position": "C",
        "pts": 26.4,
        "ast": 9.0,
        "reb": 12.4,
        "fg_pct": 0.583
    },
    {
        "search_key": "kevin durant",
        "full_name": "Kevin Durant",
        "team": "Phoenix Suns",
        "position": "F",
        "pts": 27.1,
        "ast": 5.0,
        "reb": 6.6,
        "fg_pct": 0.523
    },
    {
        "search_key": "jayson tatum",
        "full_name": "Jayson Tatum",
        "team": "Boston Celtics",
        "position": "F",
        "pts": 26.9,
        "ast": 4.9,
        "reb": 8.1,
        "fg_pct": 0.471
    },
    {
        "search_key": "shai gilgeous alexander",
        "full_name": "Shai Gilgeous-Alexander",
        "team": "Oklahoma City Thunder",
        "position": "G",
        "pts": 30.1,
        "ast": 6.2,
        "reb": 5.5,
        "fg_pct": 0.535
    },
    {
        "search_key": "victor wembanyama",
        "full_name": "Victor Wembanyama",
        "team": "San Antonio Spurs",
        "position": "C-F",
        "pts": 21.4,
        "ast": 3.9,
        "reb": 10.6,
        "fg_pct": 0.465
    },
    {
        "search_key": "anthony edwards",
        "full_name": "Anthony Edwards",
        "team": "Minnesota Timberwolves",
        "position": "G",
        "pts": 25.9,
        "ast": 5.1,
        "reb": 5.4,
        "fg_pct": 0.461
    },
    {
        "search_key": "cooper flagg",
        "full_name": "Cooper Flagg",
        "team": "Prospecto / Sin Debut NBA",
        "position": "F",
        "pts": 0.0,
        "ast": 0.0,
        "reb": 0.0,
        "fg_pct": 0.000
    },
    {
        "search_key": "karim lopez",
        "full_name": "Karim López",
        "team": "Prospecto / Sin Debut NBA",
        "position": "F",
        "pts": 0.0,
        "ast": 0.0,
        "reb": 0.0,
        "fg_pct": 0.000
    }
]

TEAM_METRICS = {
    "atl": {"name": "Atlanta Hawks", "off": 116.5, "def": 118.0, "net": -1.5},
    "bos": {"name": "Boston Celtics", "off": 122.2, "def": 110.6, "net": 11.6},
    "bkn": {"name": "Brooklyn Nets", "off": 111.0, "def": 115.2, "net": -4.2},
    "cha": {"name": "Charlotte Hornets", "off": 108.5, "def": 116.8, "net": -8.3},
    "chi": {"name": "Chicago Bulls", "off": 112.3, "def": 113.8, "net": -1.5},
    "cle": {"name": "Cleveland Cavaliers", "off": 117.0, "def": 110.2, "net": 6.8},
    "dal": {"name": "Dallas Mavericks", "off": 117.9, "def": 112.5, "net": 5.4},
    "den": {"name": "Denver Nuggets", "off": 118.5, "def": 111.2, "net": 7.3},
    "det": {"name": "Detroit Pistons", "off": 110.2, "def": 118.4, "net": -8.2},
    "gsw": {"name": "Golden State Warriors", "off": 117.8, "def": 113.5, "net": 4.3},
    "hou": {"name": "Houston Rockets", "off": 114.2, "def": 111.0, "net": 3.2},
    "ind": {"name": "Indiana Pacers", "off": 120.5, "def": 117.2, "net": 3.3},
    "lac": {"name": "LA Clippers", "off": 116.2, "def": 112.0, "net": 4.2},
    "lal": {"name": "Los Angeles Lakers", "off": 115.4, "def": 112.1, "net": 3.3},
    "mem": {"name": "Memphis Grizzlies", "off": 113.0, "def": 112.4, "net": 0.6},
    "mia": {"name": "Miami Heat", "off": 112.8, "def": 111.5, "net": 1.3},
    "mil": {"name": "Milwaukee Bucks", "off": 116.0, "def": 114.0, "net": 2.0},
    "min": {"name": "Minnesota Timberwolves", "off": 114.5, "def": 108.4, "net": 6.1},
    "nop": {"name": "New Orleans Pelicans", "off": 115.8, "def": 111.8, "net": 4.0},
    "nyk": {"name": "New York Knicks", "off": 117.2, "def": 111.0, "net": 6.2},
    "okc": {"name": "Oklahoma City Thunder", "off": 119.5, "def": 109.5, "net": 10.0},
    "orl": {"name": "Orlando Magic", "off": 111.2, "def": 109.0, "net": 2.2},
    "phi": {"name": "Philadelphia 76ers", "off": 115.0, "def": 113.2, "net": 1.8},
    "phx": {"name": "Phoenix Suns", "off": 117.0, "def": 113.2, "net": 3.8},
    "por": {"name": "Portland Trail Blazers", "off": 109.5, "def": 117.5, "net": -8.0},
    "sac": {"name": "Sacramento Kings", "off": 116.5, "def": 114.8, "net": 1.7},
    "sas": {"name": "San Antonio Spurs", "off": 112.0, "def": 116.0, "net": -4.0},
    "tor": {"name": "Toronto Raptors", "off": 111.5, "def": 117.0, "net": -5.5},
    "uta": {"name": "Utah Jazz", "off": 113.5, "def": 119.0, "net": -5.5},
    "was": {"name": "Washington Wizards", "off": 109.8, "def": 119.2, "net": -9.4}
}

@app.get("/")
def read_index():
    return FileResponse('index.html')

@app.get("/api/teams-list")
def get_teams_list():
    teams = [{"id": k, "name": v["name"]} for k, v in TEAM_METRICS.items()]
    return {"teams": teams}

@app.get("/api/todays-games")
def get_todays_games():
    return {"games": [
        {"home": "lal", "away": "bos", "home_name": "Los Angeles Lakers", "away_name": "Boston Celtics", "status": "20:30 EST", "is_live": False},
        {"home": "gsw", "away": "den", "home_name": "Golden State Warriors", "away_name": "Denver Nuggets", "status": "EN VIVO - Q3", "is_live": True}
    ]}

@app.get("/api/predict")
def predict_matchup(home_team: str = "lal", away_team: str = "bos"):
    h_key, a_key = home_team.lower(), away_team.lower()
    h = TEAM_METRICS.get(h_key, {"name": home_team.upper(), "off": 112.0, "def": 112.0, "net": 0.0})
    a = TEAM_METRICS.get(a_key, {"name": away_team.upper(), "off": 112.0, "def": 112.0, "net": 0.0})

    diff = (h["net"] + 2.5) - a["net"]
    prob_h = max(0.05, min(0.95, 1 / (1 + 10 ** (-diff / 10))))
    prob_a = 1.0 - prob_h

    return {
        "matchup": f"{h['name']} vs {a['name']}",
        "predictions": {
            h['name']: f"{round(prob_h * 100, 1)}%",
            a['name']: f"{round(prob_a * 100, 1)}%"
        },
        "stats_chart": {
            "teams": [h['name'], a['name']],
            "off_rating": [h["off"], a["off"]],
            "def_rating": [h["def"], a["def"]],
            "net_rating": [h["net"], a["net"]]
        },
        "analysis": f"Análisis de eficiencia: {h['name']} (Net {h['net']}) vs {a['name']} (Net {a['net']})."
    }

@app.get("/api/players/suggest")
def suggest_players(q: str = ""):
    clean_q = normalize_text(q)
    if not clean_q or len(clean_q) < 2:
        return {"suggestions": []}
    
    # Sugiere ÚNICAMENTE nombres que existen dentro de la fuente de verdad
    matches = [
        player["full_name"] for player in PLAYERS_DATABASE
        if clean_q in player["search_key"] or clean_q in normalize_text(player["full_name"])
    ]
    return {"suggestions": matches[:6]}

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    clean_q = normalize_text(player_name)
    
    # Busca la coincidencia exacta dentro de la fuente de verdad
    for player in PLAYERS_DATABASE:
        if clean_q in player["search_key"] or player["search_key"] in clean_q or clean_q in normalize_text(player["full_name"]):
            return player

    # Respuesta transparente cuando un jugador no está en el registro
    return {
        "full_name": player_name.title(),
        "team": "Jugador Sin Registro Oficial",
        "position": "N/A",
        "pts": 0.0,
        "ast": 0.0,
        "reb": 0.0,
        "fg_pct": 0.000
    }
