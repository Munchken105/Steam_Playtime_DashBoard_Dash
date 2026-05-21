from dash import Dash, html, dcc
import json
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import plotly.express as px

#TODO Sepreate Steam Calls into its own file (make a wraper bassicaly)

#TODO: Make a page to view games I didnt play

#TODO: make a page where i can view and add stuff to the backlog

#TODO:

#active virtual enviorment source .venv/bin/activate



load_dotenv()

#STEAM API KEYS AND MY STEAM ID
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

#data
games_url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/" #the base url with no parameters
param = { #the parameters im going to feed the url 
    "key": STEAM_API_KEY,
    "steamid" : STEAM_ID,
    "format": "json",
    "include_appinfo": True,
    "include_played_free_games": True
}

#send a request and store the response in a var
response = requests.get(games_url, params=param)

#convert the json to python data
games_data = response.json()

#get all games it games is a list of dictionarys
games = games_data["response"]["games"]

#loop to get all global achivment percentages data for each game owned

achievement_url = "https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"

#place all achievements in a dict to refernce the data later, key = appid and values = achievements
achievement_dict = {}

completion_list = []

for game in games:
    appid = game["appid"]
    game_name = game.get("name", "Unkown Game")
    
    achievement_param = {
        "key": STEAM_API_KEY,
        "steamid": STEAM_ID,
        "appid": appid
    }

    #send a request
    response = requests.get(achievement_url, params=achievement_param)
    
    #parse the request
    achievement_data = response.json()

    if "playerstats" in achievement_data:
        achievements = achievement_data["playerstats"].get("achievements", [])

        achievement_dict[appid] = {
            "game_name" : game_name,
            "achievements" : achievements
        }

        total_achievements = len(achievements)

        if total_achievements > 0:
            unlocked = sum(achievement["achieved"] for achievement in achievements)
            completion_percent = (unlocked / total_achievements) * 100

            completion_list.append({
                "game_name" : game_name,
                "appid" : appid,
                "unlocked" : unlocked,
                "total" : total_achievements,
                "completion_percent": completion_percent
            })

df = pd.DataFrame(completion_list)

df = df.sort_values(by="completion_percent", ascending=False)

fig = px.bar(
    df.head(10),
    x = 'completion_percent',
    y = 'game_name',
    title = "Steam Achievement Completion Per Game",
    orientation="h",
    labels = {
        "game_name" : "Game",
        "completion_percent" : "Completion %"
    },
    hover_data = ["unlocked", "total"]
    )

fig.update_layout(yaxis=dict(autorange="reversed"))


#inililizae dash app
app = Dash(__name__)

#app layout
app.layout = html.Div([
    html.H1("Steam Achievement Dashboard"),
    html.P(f"Games checked: {len(achievement_dict)}"),
    dcc.Graph(figure=fig)

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)