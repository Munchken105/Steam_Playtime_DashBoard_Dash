import requests
import json
#TODO: implement Steam API Wrapper

class SteamAPI:
    def __init__(self,api_key,steam_id):
        self.api_key = api_key
        self.steam_id = steam_id
        self.base_url = "https://api.steampowered.com"

    #return all games of the steam user
    def GetOwnedGames(self):
        
        games_url = f"{self.base_url}/IPlayerService/GetOwnedGames/v0001/"
        
        param = { #the parameters im going to feed the url 
            "key": self.api_key,
            "steamid" : self.steam_id,
            "format": "json",
            "include_appinfo": True,
            "include_played_free_games": True
        }

        #send a request and store the response in a var
        response = requests.get(games_url, params=param)
        
        #convert the json to python data
        games_data = response.json()

        #get all games it games is a list of dicts
        games = games_data.get("response", {}).get("games", [])

        return games

    #returns achievements of the appid specified
    def GetPlayerAchievements(self, appid):
        
        achievements_url = f"{self.base_url}/ISteamUserStats/GetPlayerAchievements/v0001/"
        
        params = {
            "key": self.api_key,
            "steamid": self.steam_id,
            "appid": appid
        }
        #send request and store response
        response = requests.get(achievements_url,params=params)
        
        achievement_data = response.json()
        
        achievements = achievement_data.get("playerstats", {}).get("achievements", [])
        
        return achievements
        
    #returns games that the user hasnt played in a list of dict key being app id and value being title list of dict is good for data frames
    # [key = appid, value = gametitle]
    def GamesNotPlayed(self):
        
       owned_games = self.GetOwnedGames()

       unplayed_games = []

       for game in owend_games:

        appid = game["appid"]
        game_title = game.get("name", "Unkown Name")

        playtimme = game.get("playtime_forever",0)

        if playtimme == 0:
            unplayed_games.append({
                "appid": appid,
                "name": game_title
            })
       
       return unplayed_games

    def GetSteamID(self):
        return self.steam_id
        

        
