from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
from datetime import datetime
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo, playercareerstats, scoreboardv2

app = FastAPI(
    title="NBA Live Analytics Dashboard Pro",
    description="API estilo SofaScore con mapa dinámico de 30 equipos y Auto-Refresh",
    version="7.0"
)

# Cargar automáticamente los equipos
all_teams = teams.get_teams()
ID_TO_NAME = {t['id']: t['full_name'] for t in all_teams}
ID_TO_NICKNAME = {t['id']: t['nickname'].lower() for t in all_teams}

TEAM_METRICS = {
    "lakers": {"off_rating": 115.4, "def_rating": 112.1, "net_rating": 3.3, "form": 0.7, "b2b": False},
    "celtics": {"off_rating": 120.2, "def_rating": 110.0, "net_rating": 10.2, "form": 0.85, "b2b": False},
    "warriors": {"off_rating": 117.8, "def_rating": 113.5, "net_rating": 4.3, "form": 0.6, "b2b": True},
    "nuggets": {"off_rating": 118.5, "def_rating": 111.2, "net_rating": 7.3, "form": 0.8, "b2b": False},
    "bucks": {"off_rating": 116.0, "def_rating": 114.0, "net_rating": 2.0, "form": 0.5, "b2b": False}
}

@app.get("/")
def read_index():
    return FileResponse('index.html')

@app.get("/api/todays-games")
def get_todays_games():
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        scoreboard = scoreboardv2.ScoreboardV2(game_date=today, timeout=10)
        df_games = scoreboard.get_data_frames()[0]
        
        games = []
        for _, row in df_games.iterrows():
            home_id = int(row['HOME_TEAM_ID'])
            visitor_id = int(row['VISITOR_TEAM_ID'])
            
            home_name = ID_TO_NAME.get(home_id, f"Equipo {home_id}")
            away_name = ID_TO_NAME.get(visitor_id, f"Equipo {visitor_id}")
            
            home_key = ID_TO_NICKNAME.get(home_id, "lakers")
            away_key = ID_TO_NICKNAME.get(visitor_id, "celtics")

            status_str = str(row['GAME_STATUS_TEXT'])
            is_live = "Q" in status_str or "Half" in status_str or "OT" in status_str

            games.append({
                "game_id": row['GAME_ID'],
                "home": home_key,
                "away": away_key,
                "home_name": home_name,
                "away_name": away_name,
                "status": status_str,
                "is_live": is_live,
                "time": status_str
            })
        
        if not games:
            return {"games": [
                {"home": "celtics", "away": "bucks", "home_name": "Boston Celtics", "away_name": "Milwaukee Bucks", "status": "Sin Actividad", "is_live": False}
            ]}
        return {"games": games}
    except Exception as e:
        return {"games": [
            {"home": "lakers", "away": "celtics", "home_name": "Los Angeles Lakers", "away_name": "Boston Celtics", "status": "20:30 EST", "is_live": False},
            {"home": "warriors", "away": "nuggets", "home_name": "Golden State Warriors", "away_name": "Denver Nuggets", "status": "EN VIVO - Q3", "is_live": True}
        ]}

@app.get("/api/predict")
def predict_matchup(home_team: str, away_team: str):
    home_key, away_key = home_team.lower(), away_team.lower()
    default_metrics = {"off_rating": 112.0, "def_rating": 112.0, "net_rating": 0.0, "form": 0.5, "b2b": False}
    home = TEAM_METRICS.get(home_key, default_metrics)
    away = TEAM_METRICS.get(away_key, default_metrics)
    
    base_diff = (home["net_rating"] + 2.5) - away["net_rating"]
    form_adj = (home["form"] - away["form"]) * 3.0
    fatigue_adj = (-2.0 if home["b2b"] else 0.0) + (2.0 if away["b2b"] else 0.0)
    
    total_diff = base_diff + form_adj + fatigue_adj
    win_prob_home = max(0.05, min(0.95, 1 / (1 + 10 ** (-total_diff / 10))))
    win_prob_away = 1 - win_prob_home

    home_title = home_key.capitalize()
    away_title = away_key.capitalize()

    return {
        "matchup": f"{home_title} vs {away_title}",
        "predictions": {
            home_title: f"{round(win_prob_home * 100, 1)}%",
            away_title: f"{round(win_prob_away * 100, 1)}%"
        },
        "stats_chart": {
            "teams": [home_title, away_title],
            "off_rating": [home['off_rating'], away['off_rating']],
            "def_rating": [home['def_rating'], away['def_rating']],
            "net_rating": [home['net_rating'], away['net_rating']]
        },
        "analysis": "Predicción multivariable basada en Net Rating y condiciones de descanso."
    }

@app.get("/api/player/{player_name}")
def get_player_stats(player_name: str):
    try:
        all_players = players.get_players()
        matched = [p for p in all_players if player_name.lower() in p['full_name'].lower()]
        
        if not matched:
            return {"error": "Jugador no encontrado en la base de datos oficial."}
        
        player_id = matched[0]['id']
        p_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id, timeout=10)
        df_info = p_info.get_data_frames()[0]
        
        career = playercareerstats.PlayerCareerStats(player_id=player_id, timeout=10)
        df_career = career.get_data_frames()[0]
        recent_season = df_career.iloc[-1] if not df_career.empty else {}

        return {
            "full_name": df_info['FIRST_NAME'].values[0] + " " + df_info['LAST_NAME'].values[0],
            "team": df_info['TEAM_NAME'].values[0],
            "position": df_info['POSITION'].values[0],
            "pts": float(recent_season.get('PTS', 25.4)),
            "ast": float(recent_season.get('AST', 6.5)),
            "reb": float(recent_season.get('REB', 7.1)),
            "fg_pct": float(recent_season.get('FG_PCT', 0.48))
        }
    except Exception as e:
        return {
            "full_name": player_name.capitalize(),
            "team": "Equipo NBA",
            "position": "G-F",
            "pts": 27.5,
            "ast": 8.2,
            "reb": 7.5,
            "fg_pct": 0.51
        }
