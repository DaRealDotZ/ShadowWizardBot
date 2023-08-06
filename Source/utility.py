import discord
import itertools

from discord import Color

def get_all_caps(string):
  lu_sequence = ((c.lower(), c.upper()) for c in string)
  array = [''.join(x) for x in itertools.product(*lu_sequence)]
  returnArray = []
  
  for v in array:
    if (v != string.lower()):
      returnArray.insert(len(returnArray)+1,v)
      
  return returnArray

async def send_message_in_dm(ctx, message):
  channel = await ctx.author.create_dm()
  
  await channel.send(message)

async def send_embed_in_dm(ctx, embedTitle, embedDescription):
  embed = discord.Embed(
    title = embedTitle,
    description = embedDescription,
    colour = Color.pink()
  )

  channel = await ctx.author.create_dm()

  await channel.send(embed = embed)