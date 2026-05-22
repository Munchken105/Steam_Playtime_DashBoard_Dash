from dash import Dash, html, dcc, Input, Output, callback
import json
import pandas as pd
import os
from dotenv import load_dotenv
import requests
import plotly.express as px
from steam_api import SteamAPI

#TODO: Make a page to view games I didnt play

#TODO: make a page where i can view and add stuff to the backlog (in progress)

#TODO: work on making tabs in the app using tabs to switch between back log manager and graphs 

#TODO: Make Feature to see friends graphs

#active virtual enviorment source .venv/bin/activate


#loads the .env file
load_dotenv()



#STEAM API KEYS AND MY STEAM ID
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

steam = SteamAPI(STEAM_API_KEY,STEAM_ID)


#get all games it games is a list of dictionarys
games = steam.GetOwnedGames()

#loop to get all global achivment percentages data for each game owned



#place all achievements in a dict to refernce the data later, key = appid and values = achievements
achievement_dict = {}

completion_list = []

for game in games:
    appid = game["appid"]
    
    #get the name of the game if there is no name than call it Unknown Game
    game_name = game.get("name", "Unknown Game")
    

    achievements = steam.GetPlayerAchievements(appid)

    #if i have a achivement in x game than update the achievement dict
    if achievements:
        achievement_dict[appid] = {
            "game_name": game_name,
            "achievements": achievements
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
if not df.empty:
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


    html.H1("Steam Dashboard"),
    
    dcc.Tabs([
        dcc.Tab(label="Graphs",children=[
            html.P(f"Games checked: {len(achievement_dict)}"),
            dcc.Graph(figure=fig)
        ]),

        dcc.Tab(label="BackLog",children=[
            html.H2("Backlog"),
            html.P("Blacklog manger place holder")

        ]),
    ]),

    

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)