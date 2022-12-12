from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request
import re


class CricAPI:

    def init(self, url):
        url_text = requests.get(url).text
        soup = BeautifulSoup(url_text, "html.parser")
        return(soup)

    def get_url_fromid(self, matchid):
        url_text = requests.get("https://www.espncricinfo.com").text
        soup = BeautifulSoup(url_text, "html.parser")
        links = []
        for link in soup.findAll('a'):
            links.append(link.get('href'))
        reqLink = [(id) for id in links if re.search(str(matchid), id)][0]
        reqLink = "https://www.espncricinfo.com" + '/'.join(reqLink.split("/")[:-1]) + "/full-scorecard"
        return(reqLink)




    def Scorecard_batting(self, team, url):
        soup = self.init(url)
        playerDict = {}

        for i in range(2):
            players = soup.find_all("tbody")[i*2]
            players = players.find_all("td")
            j = 0
            for i in range(0, len(players)):
                name = players[j].text

                #urlVal = players[j].find("a").get("href")
                if name == "Extras":
                    break
                if not(players[j].find("a") and players[j].find("a").get("href")):
                    j = j + 1
                    continue

                playerDict[name] = {"name": name,
                                    "info": players[j + 1].text,
                                    "runs": players[j + 2].text,
                                    "balls": players[j + 3].text,
                                    "fours": players[j + 5].text,
                                    "sixs": players[j + 6].text,
                                    "SR": players[j + 7].text,
                                    "href": players[j].find("a").get("href").split("/")[-1]
                                    }
                j = j + 8
        return(playerDict)

    def player_score(self, player_info,url):
        allPlayerInfo = self.Scorecard_batting(2)

        player = [(key) for key in allPlayerInfo if re.search(player_info, allPlayerInfo[key]["href"])]
        return(allPlayerInfo[player[0]])

    def get_playing11_display(self, url):
        reqLink = '/'.join(url.split("/")[:-1]) + "/match-playing-xi"
        soup = self.init(reqLink)
        players = soup.find_all("tbody")[0].find_all("a")

        i = 0
        playerList = []
        for player in players:
            if i < 22 and player.get('href'):
                playerList.append({"name" : player.find("span").text, "data" : player.get('href').split("/")[-1]})
                i = i+1
        return playerList

    def get_playing11(self, url):
        reqLink = '/'.join(url.split("/")[:-1]) + "/match-playing-xi"
        soup = self.init(reqLink)
        players = soup.find_all("tbody")[0].find_all("a")
        teams = soup.find_all("thead")[0].find_all("th")
        teamList = []
        for team in teams:
            if team.find("span"):
                teamList.append(team.find("span").text)
        #print(teams)

        i = 0
        playerList = []
        for player in players:
            if i < 22 and player.get('href'):
                playerList.append(player.find("span").text)
                i = i+1
        playerDict = [{"team" : teamList[0], "players" : playerList[0::2]}, {"team" : teamList[0], "players" : playerList[1::2]}]
        return(playerDict)



if __name__ == "__main__":
    cricAPI = CricAPI()
    playerList = cricAPI.get_playing11(cricAPI.get_url_fromid(1324528))




