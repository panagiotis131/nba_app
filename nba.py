import requests
import pymongo
import pandas as pd
from io import StringIO


download_url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-elo/nbaallelo.csv"

response = requests.get(download_url)
response.raise_for_status()

data = StringIO(response.text)

nba = pd.read_csv(data)

myclient = pymongo.MongoClient(
    "mongodb://mongodb_container:27017/",
    username="root",
    password="rootpassword",
)

mydb = myclient["nbadb"]
mycol = mydb["games"]

records = nba.to_dict("records")
mycol.insert_many(records)

home_wins = 0
total_knicks_games = 0
for record in mycol.find({"team_id": "NYK"}):
    total_knicks_games += 1
    if record["game_location"] == "H" and record["game_result"] == "W":
        home_wins += 1
print("Knicks home win percentage is ", 100 * (home_wins/total_knicks_games), "%")
