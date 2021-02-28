import discord  # a python documentation
import os
import requests
import json
import random
from replit import db
from discord.ext import commands
from trigger import keep_alive

bot= commands.Bot(description="test", command_prefix="!")
client=discord.Client()






sad_words =["dukhi","sad","depressed","unhappy","gussa","angry","miserable","badhaal","depressing","bakwaas","jhand"]

starter_encouragements =[
  "Abe kuch nahi hoga, chill maar bhai!",
  "Tu champ hai bhai,tension na le!",
  "Jindagi sabki jhand hai, bas khush reh jeevan me!",
  "Cheer up dude!",
  "Engineering jhel raha hai tu, baaki sabkuch jhel lega tu life me!",
  "Jindagi me Ups and Downs hote rehte hain mere bhai, bas chalta reh, sab sahi hoga!"
]

shayari =[
  "Kuch paristhityon ko dekh ghabra jau to kayar na samajhna, 2-3 shayari kya maar di, mujhe shaayar na samajhna",
  "Muskurana har ladki ki adaa hai, jo use pyaar samjhe wo pakka gadha hai",
  "COVID ke bharose ab CG nahi milne wala hai, Ab to padh lo salaon kyuki college khulne wala hai",
  "Rahiman dhaaga prem ka, mat todo chatkae, online sem ke maje khtm, padh le mere bhai",
  "Mohabbat Na Sahi Mukadama Hi Kar De,Tareekh-Dar-Tareekh Mulakaat To Hogi.",
  "Palat Dunga Saari Duniya Main Ai Khuda,Bas iss sem ka exam online kara de",
  "Humari Kismat Hi Kuchh Aisi Nikli Ghalib, Zamin Mili To Banjar Aur Admin Mila To Kanjar.",
  "Ek Boond Se Kabhi Saagar Nahi Banta,Raat Din Rone Se Muqaddar Nahin Banta,Patana Hai To Poora Hostel Pataao,Ek ko Pataa Kar Koi Sikandar Nahin Banta."


                                                                   
]

def get_quote():
  response=requests.get("https://zenquotes.io/api/random")
  json_data =json.loads(response.text)
  quote=json_data[0]['q'] + " -" +json_data[0]['a']
  return(quote)

def get_joke():
  response=requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data =json.loads(response.text)
  quote=json_data["setup"]+" "+json_data["punchline"]
  return(quote)

def get_image():
  response=requests.get("https://pixabay.com/api/?key="+os.getenv('KEY')+"&q=random&image_type=photo")
  json_data =response.json()
  r=random.randint(0,20)
  img=json_data["hits"][r]["webformatURL"]
  return(img)



def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements=db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"]= encouragements
  else:
    db["encouragements"]=[encouraging_message]

def delete_encouragements(index):
  encouragements= db["encouragements"]
  if len(encouragements)> index:
    del encouragements[index]
    db["encouragements"]= encouragements

@client.event
async def on_ready():
  print('You have logged in as {0.user}'.format(client))

@bot.command()



@client.event
async def on_message(message):
  if message.author==client.user:
    return
  
  msg=message.content
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')
 
  if message.content.startswith('$gyaan'):
    quote=get_quote()
    await message.channel.send(quote)

    
  if message.content.startswith('$joke pls'):
    quote=get_joke()
    await message.channel.send(quote)
  if message.content.startswith('$img pls'):
    quote=get_image()
    await message.channel.send(quote)
  
  options=starter_encouragements;
  if "encouragements" in db.keys():
    options=options+db["encouragements"]


  if any(word in msg for word in sad_words ):
    await message.channel.send(random.choice(options))
  
  if msg.startswith("$shayari"):
  
      await message.channel.send(random.choice(shayari))
  
  
  if msg.startswith("$new"):
    encouraging_message= msg.split("$new ",1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouragement added")


  if msg.startswith("$del"):
    encouraging_message=[]
    if "encouragements" in db.keys():
      index=int(msg.split("$del",1)[1])
      delete_encouragements(index)
      encouragements=db["encouragements"]
    await message.channel.send(encouragements)

  


keep_alive()
client.run(os.getenv('TOKEN'))
