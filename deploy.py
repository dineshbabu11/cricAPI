from bs4 import BeautifulSoup
import requests
from flask import Flask, url_for, render_template, request
from CricAPI import *
import re

app = Flask(__name__)

cricAPI = CricAPI()
@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/player_score")
def player_score():
    matchid = request.args['matchid']
    playerid = request.args['playerid']

    allPlayerInfo = cricAPI.Scorecard_batting(2, cricAPI.get_url_fromid(matchid))
    allPlayerInfo.update(cricAPI.Scorecard_batting(1, cricAPI.get_url_fromid(matchid)))
    allPlayers = []
    for key in allPlayerInfo:
        allPlayers.append(key)
    players = [(key) for key in allPlayerInfo if re.search(playerid, allPlayerInfo[key]['href'], re.IGNORECASE)]

    if players:
        return (allPlayerInfo[players[0]])
    else:
        return []

@app.route("/players_display")
def players_display():
    matchid = request.args["matchid"]
    playerList = cricAPI.get_playing11_display(cricAPI.get_url_fromid(matchid))
    return(render_template('players.html', players=playerList))

@app.route("/players")
def players():
    matchid = request.args["matchid"]
    return(cricAPI.get_playing11(cricAPI.get_url_fromid(matchid)))

if __name__ == "__main__":
    app.run(port='5002', debug=True)