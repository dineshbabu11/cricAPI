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
        reqLink = [(id) for id in links if re.search(str(matchid), id) and re.search("live", id)][0]
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


    def players_info_no_scorecard(self, team, url):
        soup = self.init(url)
        playerList = []
        playerList_noBat = []
        players = soup.find_all("tbody")[(team-1)*2]
        players = players.find_all("td")
        players_noBat = [(player) for player in players if player.find("div") and player.find("div").find("strong") and player.find("div").find("strong").text and re.search("Did not bat", player.find("div").find("strong").text)]
        if players_noBat:
            players_noBat = players_noBat[0]
            players_noBat = players_noBat.find_all('a')
            for player in players_noBat:
                if player.find('span'):
                    playerList_noBat.append({"name": player.find('span').find('span').text.replace(",", ""), "data": player.get('href').split("/")[-1]})

        j = 0
        for i in range(0, len(players)):
            name = players[j].text
            if name == "Extras":
                break
            if not (players[j].find("a") and players[j].find("a").get("href")):
                j = j + 1
                continue
            playerList.append({"name": name , "data": players[j].find("a").get("href").split("/")[-1]})
            j = j + 8

        for player in playerList_noBat:
            playerList.append(player)

        return playerList


