
import discord
import urllib.request
from bs4 import BeautifulSoup
import csv
import random

#from datetime import datetime
import datetime
from datetime import date
from discord.ext import commands


#Discord Bot ID [censored]
TOKEN = "#######################################"

#Create the bot client
client = discord.Client()




LEAGUES = {"cl" : "uefa.champions",
           "el" : "uefa.europa",
           "lcup" : "eng.league_cup",
           "facup" : "eng.fa",
           "pl" : "eng.1",
           "int" : "fifa.friendly"}

LEAGUENAMES = {"cl" : "**UEFA Champions League",
               "el" : "**UEFA Europa League",
               "lcup" : "**English Carabao Cup",
               "facup" : "**English FA Cup",
               "pl" : "**English Premier League",
               "int" : "**International Friendly"}

LEAGUEMAX = {"cl" : 4,
             "el" : 4,
             "lcup" : -1,
             "facup" : -1,
             "pl" : 20,
             "int" : -1}





#########################################################################
#############################Wrong Usage#################################
#########################################################################

def wrongUsage():
    msg = "```That is the wrong usage!\n\n"
    msg += "Commands:\n"
    msg += "?? [competition] - Gets today's fixtures\n"
    msg += "?? [competition] next - Gets the next fixtures\n"
    msg += "?? [competition] prev - Gets the previous fixtures\n"
    msg += "?? [competition] table - Gets the table standings\n"
    msg += "?? [competition] tops - Gets the top 5 scorers/assists\n"
    msg += "?? [competition] news - Gets the latest news\n"
    msg += "?? [competition] [date] - Gets a specific fixture, date format in YYYYmmdd, e.g. 20181211\n"
    msg += "?? transfers - Gets latest EPL transfers and latest transfer news\n\n"
    msg += "Available Competitions:\n"
    msg += "cl - Champions League\n"
    msg += "el - Europa League\n"
    msg += "pl - English Premier League\n"
    msg += "facup - English FA Cup\n"
    msg += "lcup - English League Cup\n"
    msg += "int - International Friendlies\n\n"
    msg += "If you want to add more competitions or features, please contact Nadramon.\n"
    msg += "There are known bugs with English Premier League as of now.```"
    return msg



#########################################################################
#############################League Code#################################
#########################################################################

def getFixtures(comp, now, rType = 0):
    msg = ""

    while True:
        urlpage = "https://www.espn.com/soccer/fixtures/_/date/"
        urlpage += now.strftime("%Y%m%d")
        urlpage += "/league/"
        urlpage += LEAGUES[comp]
        page = urllib.request.urlopen(urlpage)
        soup = BeautifulSoup(page, 'html.parser')

        scheduleEmpty = soup.findAll('p', attrs={"id" : "noScheduleContent"})
        bugFixer = soup.findAll('h2', attrs={"class" : "table-caption"})

        if comp == "pl":
            magic = bugFixer[0].text.strip()
            magic = magic [-2:]
            actual = now.strftime("%Y%m%d")
            if magic[0] == " ":
                magic = "0" + magic[1]
            if actual[-2:] !=  magic:
                scheduleEmpty = [1]




        if (len(scheduleEmpty) != 0 and rType == 0):
            msg += LEAGUENAMES[comp]
            msg += " Fixtures**\n"
            msg += now.strftime("**%dth %b %Y** \n\n")
            msg += "*There are no matches today.*"
            break
        elif(len(scheduleEmpty) == 0 or rType == 0):
            teamNames = soup.findAll('a', attrs={"class" : "team-name"})
            scores = soup.findAll('span', attrs={"class" : "record"})
            y = 0
            longestName = 0
            msg += LEAGUENAMES[comp]
            if scores[0].text.strip() == "v":
                msg += " Fixtures**\n"
            else:
                msg += " Results**\n"
            msg += now.strftime("**%dth %b %Y** \n\n")
            for x in range(0, len(teamNames), 2):
                if len((teamNames[x].text.strip())[:-4]) > longestName:
                    longestName = len((teamNames[x].text.strip())[:-4])
            longestName += 5
            for x in range(0, len(teamNames), 2):
                t1 = (teamNames[x].text.strip())[:-4]
                msg += t1
                msg += "\t { "
                msg += scores[y].text.strip()
                msg += " } \t"
                msg += (teamNames[x+1].text.strip())[:-4]
                msg += "\n"
                y += 1
            break

        else:
            now = now + datetime.timedelta(days=rType)

    return msg


def getNews(comp):
    msg = ""
    urlpage = "https://www.espn.com/soccer/league/_/name/"
    urlpage += LEAGUES[comp]
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')
    news = soup.findAll('a', attrs={"class" : " realStory"})

    msg += LEAGUENAMES[comp]
    msg += " News**\n\n"

    newsCount = 5
    if len(news) < 5:
        newsCount = len(news)
    for x in range(newsCount):
        msg += "*- "
        msg += news[x].text.strip()
        msg += "*\n\t<https://www.espn.com"
        msg += news[x]['href']
        msg += ">\n"
    return msg



def getTable(comp):
    msg = ""
    urlpage = "https://www.espn.com/soccer/standings/_/league/"
    urlpage += LEAGUES[comp]
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')

    teams = soup.findAll('span', attrs={"class" : "hide-mobile"})
    numbers = soup.findAll('span', attrs={"class" : "stat-cell"})
    
    y = 0
    pos = 1
    asciiVal = 65
    
    msg += LEAGUENAMES[comp]
    msg += "**\n"

    if LEAGUEMAX[comp] == -1:
        msg += "This competition does not support tables."
        return msg
    
    if LEAGUEMAX[comp] < 10:
        msg += "**Group A**\n"
    msg += "Pos | GP |  Pts  | Club\n"
    for x in range(0, len(teams)):
        if pos > LEAGUEMAX[comp]:
            pos = 1
            asciiVal += 1
            msg += "\n**Group "
            msg += chr(asciiVal)
            msg += "**\n"
            msg += "Pos | GP |  Pts  | Club\n"
        msg += str(pos)
        temp = str(pos)
        if len(temp) == 1:
            msg += "     "
            if temp[0] == "1":
                msg += " "
        else:
            for z in range(0, len(temp)):
                if temp[z] == "1":
                    msg += "  "
                elif temp[z] != "0":
                    msg += " "
                else:
                    msg += " "
        msg += "|  "
        msg += numbers[y].text.strip()
        msg += "  |  "
        y += 7
        msg += numbers[y].text.strip()
        msg += "  |  "
        msg += teams[x].text.strip()
        msg += "\n"
        y += 1
        pos += 1
    return msg[:2000]


def getTops(comp):
    msg = ""
    urlpage = "https://www.espn.com/soccer/stats/_/league/"
    urlpage += LEAGUES[comp]
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')

    #date, player, club, blank, club, price
    tableData = soup.findAll('td', attrs={"class" : "Table__TD"})
    y = 0
    msg += LEAGUENAMES[comp]
    if len(tableData) == 0:
        msg += "**\nNo data available for top scorers/assists"
        return msg
    msg += " Top Scorers**\n"
    msg += "No. | GL |  Player  |  Team\n"
    for x in range(5):
        msg += str(x+1)
        if x == 0:
            msg += " "
        msg += "     |  "
        y += 4
        msg += tableData[y].text.strip()
        msg += "  |  "
        y -= 3
        msg += tableData[y].text.strip()
        msg += "  |  "
        y += 1
        msg += tableData[y].text.strip()
        msg += "\n"
        y += 3

    while True:
        if tableData[y].text.strip() == "1":
            break
        y += 5
        
    msg += "\n"
    msg += LEAGUENAMES[comp]
    msg += " Top Assists**\n"
    msg += "No. | AS |  Player  |  Team\n"
    for x in range(5):
        msg += str(x+1)
        if x == 0:
            msg += " "
        msg += "     |  "
        y += 4
        msg += tableData[y].text.strip()
        msg += "  |  "
        y -= 3
        msg += tableData[y].text.strip()
        msg += "  |  "
        y += 1
        msg += tableData[y].text.strip()
        msg += "\n"
        y += 3
        
    return msg




def getTransfers():
    urlpage = "https://www.espn.com/soccer/transfers/_/league/eng.1"
    page = urllib.request.urlopen(urlpage)
    soup = BeautifulSoup(page, 'html.parser')

    #date, player, club, blank, club, price
    tableData = soup.findAll('td', attrs={"class" : "Table__TD"})
    transferNews = soup.findAll('div', attrs={"class" : "News__Item__Headline"})
    transferNewsLink = soup.findAll('a', attrs={"class" : "News__Item"})

    y = 0
    msg = "**English Premier League Transfers**\n"
    for x in range(5):
        msg += tableData[y].text.strip()
        msg += " | ***"
        y += 1
        msg += tableData[y].text.strip()
        msg += "*** from **"
        y += 1
        t1 = tableData[y].text.strip()
        if t1[:7] == "No team":
            t1 = "Unemployment"
        else:
            t1 = t1[3:]
        msg += t1
        msg += "** moves to **"
        y += 2
        t2 = tableData[y].text.strip()
        if t2[:6] == "No team":
            t2 = t2[6:]
        else:
            t2 = t2[3:]
        msg += t2
        msg += "** for *"
        y += 1
        msg += tableData[y].text.strip()
        msg += "*\n"
        y += 1

    msg += "\n**Transfer News**\n"
    for x in range(3):
        msg = msg + "*" + transferNews[x].text.strip() + "*\n\t<" + transferNewsLink[x]['href'] + ">\n"
    return msg



#########################################################################
##############################Main Code##################################
#########################################################################


            
#Startup Bot
@client.event
async def on_ready():
    print("NadraSoccer has Started Running...")



#Every time someone message the Discord, run this code
@client.event
async def on_message(message):


    #So the bot doesn't react to itself
    if message.author == client.user:
        return


    if message.content.startswith("test"):
        await client.send_message(message.channel,"nader is gay")


    if message.content.startswith("??"):
        lowered = (message.content).lower()
        msgParts = lowered.split()
        msgLen = len(msgParts)
        if msgLen == 1 or msgLen > 3:
            msg = wrongUsage()
            await client.send_message(message.channel,msg)
            return
        elif msgParts[1] not in LEAGUES and msgParts[1] != "transfers":
            msg = wrongUsage()
            await client.send_message(message.channel,msg)
            return
        
        now = date.today()
        if msgLen == 3:
            if msgParts[2] == "next":
                now = now + datetime.timedelta(days=1)
                msg = getFixtures(msgParts[1], now, 1)
                await client.send_message(message.channel,msg)
                return
            elif msgParts[2] == "prev":
                now = now + datetime.timedelta(days=-1)
                msg = getFixtures(msgParts[1], now, -1)
                await client.send_message(message.channel,msg)
                return
            elif msgParts[2] == "table":
                msg = getTable(msgParts[1])
                await client.send_message(message.channel,msg)
                return
            elif msgParts[2] == "tops":
                msg = getTops(msgParts[1])
                await client.send_message(message.channel,msg)
                return
            elif msgParts[2] == "news":
                msg = getNews(msgParts[1])
                await client.send_message(message.channel,msg)
                return
            try:
                now = datetime.datetime.strptime(msgParts[2], "%Y%m%d").date()
                msg = getFixtures(msgParts[1], now)
                await client.send_message(message.channel,msg)
                return
            except:
                msg = wrongUsage()
                await client.send_message(message.channel,msg)
                return
        else:
            if msgParts[1] == "transfers":
                msg = getTransfers()
                await client.send_message(message.channel,msg)
                return
            else:
                msg = getFixtures(msgParts[1], now)
                await client.send_message(message.channel,msg)
                return




#Connect client with NadraSoccer Bot
client.run(TOKEN)
