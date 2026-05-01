from dash import Dash, html
import json
import panda as panda
import os
from dotenv import load_dotenv

load_dotenv()

#STEAM API KEYS AND MY STEAM ID
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

#data
games_url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/" #the base url with no parameters
param = { #the parameters im going to feed the url 
    "key": STEAM_API_KEY
    "steamid" : STEAM_ID
    "format": "json"
    "include_appinfo": True
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

for game in games:
    appid = game["appid"]
    
    achievement_param = {
        "key": STEAM_API_KEY
        "steamid": STEAM_ID
        "appid": appid
    }

    #send a request
    response = requests.get(achievement_url, params=achievement_param)
    #parse the request
    achievement_data = response.json()


    



#inililizae dash app
app = Dash(__name__)

#app layout
app.layout = [html.Div(children='Hello World')]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)