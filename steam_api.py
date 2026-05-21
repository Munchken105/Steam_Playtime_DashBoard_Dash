import requests
import json
#TODO: implement Steam API Wrapper

class SteamAPI:
    def __init__(self,api_key,steam_id):
        self.api_key = api_key
        self.steam_id = steam_id
        self.base_url = "https://api.steampowered.com"

    def GetOwnedGames(self):
        
        url = f"{self.base_url}//PlayerService/GetOwnedGames/v0001/"
        
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

        #get all games it games is a list of dicts
        games = games_data["response"]["games"]

        return games

    def GetPlayerAchievements(self, appid):
        url = f"{self.base_url}/ISteamUserStats/GetPlayerAchievements/v0001/"

        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "steamid": appid
        }

        #send request and store response
        response = requests.get(games_url,params=params)

        achievment_data = response.json()

        achievements = achievement_data["playerstats"].get("achievements", [])
        
        return achievments
        

        
