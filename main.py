#have bot send daily message using date
#have it send link and picture of the animal from message by finding 'a' tag
#have the user send a command to get a fact by having it go to the page with all the animals by letter and choosing random stuff until it gets a fact, doesnt need url or pic, would be nice tho
from discord.ext import commands, tasks
import os
import discord
import urllib.request 
from bs4 import BeautifulSoup
import datetime
import secrets
from keep_alive import keep_alive

client = discord.Client()

#print(datetime.datetime.now().minute)
  
# providing url
channelid = 801966805442101261
url = "https://animalcorner.org/"
listUrl = "https://animalcorner.org/animals/"
  
# opening the url for reading
html = urllib.request.urlopen(url)
htmlList = urllib.request.urlopen(listUrl)
  
# parsing the html file
htmlParse = BeautifulSoup(html, "html.parser")
htmlListParse = BeautifulSoup(htmlList, "html.parser")




#getting picture 
# def web_picture():
#   for para in htmlParse.find("div", attrs={"id": "featured-animal"}).find_all("img"):
#       bot_picture = para.get_text()
#       print (bot_picture)
#   return bot_picture
# web_picture()

animalList = [] #list used to store links
factList = []

#loop to get links to scrape facts
for article in htmlListParse.find("article", attrs={"class": "post-721 animals type-animals status-publish format-standard has-post-thumbnail category-uncategorized endangered-not-listed group-mammalia entry"}):
  for div in htmlListParse.find_all("div", ["one-third", "one-third first"]):
    a = div.find('a')
    print(a['href'])
    animalList.append(a["href"])
  break

#used to get paragraph for fact
def randomFact():
  factList.clear()
  x = secrets.choice(animalList)
  htmlRandFact = urllib.request.urlopen(x)
  print (x)
  htmlListParseRandFact = BeautifulSoup(htmlRandFact, "html.parser")
  for main in htmlListParseRandFact.find("main", attrs={"class": "content"}):
    for para in htmlListParseRandFact.find_all("p"):
      factList.append(para.get_text())
    break
  del factList[:3]
  del factList[-2:]
  print ("\n", factList)
  print (x)
  if '' in factList:
    factList.remove('')
  return "*"+secrets.choice(factList)+"*" +"\n"+ x



#gets rid of 'a' tag
for links in htmlParse.find_all("a"):
  links.extract()

# getting all the paragraphs
for para in htmlParse.find("div", attrs={"id": "featured-text"}).find_all("p"):
    bot_message = para.get_text()

@client.event
async def on_message(message):
  channel = client.get_channel(channelid)
  if message.author == client.user:
    return
  if message.content.startswith("$fact"):
    await channel.send(randomFact())
  # if datetime.datetime.now().minute == "20":
  #   await message.channel.send(web_message()+"\n"+url)

@tasks.loop(hours=24) 
async def send_message():
  channel = client.get_channel(channelid)
  await channel.send("**Daily Random Animal Fact!**" + "\n" + randomFact())
 
@client.event
async def on_ready():
  print("Bot online: {0.user}".format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Monkey Music'))
  send_message.start()

keep_alive()
my_secret = os.environ["TOKEN"]
client.run(my_secret)
