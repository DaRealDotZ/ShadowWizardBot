



# -------------------------------------------------------------------------------- #
# ----------------------------------- IMPORTS ------------------------------------ #
# -------------------------------------------------------------------------------- #



import discord
import itertools

import pickle
import os

from discord import Member
from discord import Color

from discord.ext import commands

from datetime import datetime
from webserver import keep_alive



# ---------------------------------------------------------------------------------- #
# ----------------------------------- VARIABLES ------------------------------------ #
# ---------------------------------------------------------------------------------- #




reactionRoles = [
  ["🟦", "He/Him"],
  ["🟪", "She/Her"],
  ["🟨", "They/Them"],
  ["⭐", "Shadow Wizard Newbie"],
  ["📔", "Artist"]
]

client = commands.Bot(command_prefix=";", case_insensitivity=True, intents= discord.Intents.all())

client.remove_command('help')

serverRules = """
**0) Breaking Discord's TOS (Terms of Service) and/or 
Discord's Community Guidelines will NOT be tolerated.
(Strike 1: Server Ban)**

**1) Harrasment, bullying, and non-civilized
arguments are prohibited.
(Strike 1: Warning, Strike 2: Timout, Strike 3: Kick, Strike 4: Soft-Ban, Strike 5: Hard-Ban)**

**2) Spamming and excessively being annoying
to others is prohibited. 
(Strike 1: Warning, Strike 2: Timout | 1-7 Day(s), Strike 3: Kick, Strike 4: Soft-Ban, Strike 5: Hard-Ban)**

**3) Sending malware/scam links in personal DM's 
and in the server is prohibited.
(Strike 1: Server Ban)**

**4) Displaying any form 
of sexual content will NOT be tolerated
(Strike 1: Soft-Ban, Strike 2: Hard-Ban)**

**5) Any form of racism, sexism, 
and overall discrimination is prohibited.
(Strike 1: Timeout | 1 Week, Strike 2: Soft-Ban, Strike 3: Hard-Ban)**

**6) Using server channels 
the way they aren't suppose to be used is prohibited.
(Strike 1: Warning, Strike 2: Second Warning, Strike 3: Timeout | 1 Day, Strike 4: Timeout | 1 Week, Strike 5: kick, Strike 6: Soft-Ban)**

**7) Inappropriate usernames, profile pictures, 
display names, etc are prohibited.
(Strike 1: Timeout | 1 Day, Strike 2: Kick, Strike 3: Soft-Ban, Strike 4: Hard-Ban)**

**8) Disturbing content 
such as Gore will NOT be tolerated.
(Strike 1: Server Ban)**

**9) False reporting using 
the ;report command is prohibited.
(Strike 1: Timeout | 1 Day, Strike 2: Kick, Strike 3: Soft-Ban, Strike 4: Hard-Ban)**

**10) Using slurs in any
context will NOT be tolerated.
(Strike 1: Warn, Strike 2: Timeout | 1 Week, Strike 3: Soft-Ban, Strike 4: Hard-Ban)**

**11) Pedophilia, Zoophilia, 
and other disturbing sexual attractions are prohibited.
(Strike 1: Hard-Ban)**

**12) Leaking yours or others 
real life information is strictly prohibited.
(Strike 1: Soft-Ban, Strike 2: Hard-Ban)**

**<------------------------------------------------>**

**THESE RULES WILL APPLY OUTSIDE OF THE SERVER!!**

**<------------------------------------------------>**

**Discord's Terms Of Service: https://discord.com/terms**
**Discord's Community Guidelines: https://discord.com/guidelines**

**<------------------------------------------------>**
## 🏆 Thank You For Reading! 🏆
"""



# --------------------------------------------------------------------------------------- #
# -------------------------------------- FUNCTIONS -------------------------------------- #
# --------------------------------------------------------------------------------------- #



def returnPossibleCaps(string):
  lu_sequence = ((c.lower(), c.upper()) for c in string)
  array = [''.join(x) for x in itertools.product(*lu_sequence)]
  returnArray = []
  
  for v in array:
    if (v != string.lower()):
      returnArray.insert(len(returnArray)+1,v)
      
  return returnArray




# --------------------------------------------------------------------------------------- #
# ------------------------------------ CLIENT EVENTS ------------------------------------ #
# --------------------------------------------------------------------------------------- #





@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name='";help" | V1.0 | Currently Moderating The Shadow Wizard Money Gang...'))
  print(f"{client.user.display_name} Is online!")

@client.event
async def on_member_join(member):
  userData = load_member_data(member.id)
  
  role = discord.utils.get(member.guild.roles, id=1118316334292406292)
  roleBan = discord.utils.get(member.guild.roles, id=1120961059990290522)

  embed = discord.Embed(
    title=f"{member.display_name} Has joined the server!",
    description=f'Welcome to the server {member.mention}!\nMake sure to read the **📜Server Rules📜**!',
    colour = Color.green(),
    timestamp = datetime.utcnow()
  )
  embed.set_thumbnail(url=member.display_avatar.url)

  if not (userData.softbanned):
    await member.add_roles(role)
  elif (userData.softbanned):
    await member.add_roles(roleBan)
  await client.get_channel(1118372347347476480).send(embed=embed)

@client.event
async def on_member_remove(member):
  embed = discord.Embed(
    title=f"{member.display_name} Has left the server...",
    description=f'Goodbye **{member.display_name}**!',
    colour = Color.red(),
    timestamp = datetime.utcnow()
  )
  embed.set_thumbnail(url=member.display_avatar.url)
  
  await client.get_channel(1118372347347476480).send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if (message_id == 1119600175984418897):
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
      role = None
      
      for reaction in reactionRoles:
        if (payload.emoji.name == reaction[0]):
          role = discord.utils.get(guild.roles, name = reaction[1])

      if (role is not None):
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if (member is not None):
          print('Added role to member')
          await member.add_roles(role)
        else: 
          print('WARNING: Could not find member.')
      else:
        print('WARNING: Could not find role.')

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if (message_id == 1119600175984418897):
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
      role = None

      for reaction in reactionRoles:
        if (payload.emoji.name == reaction[0]):
          role = discord.utils.get(guild.roles, name = reaction[1])

      if (role is not None):
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if (member is not None):
          print('Removed role from member')
          await member.remove_roles(role)
        else: 
          print('WARNING: Could not find member.')
      else:
        print('WARNING: Could not find role.')




# --------------------------------------------------------------------------------------- #
# ----------------------------------- CLIENT COMMANDS ----------------------------------- #
# --------------------------------------------------------------------------------------- #




data_filename = "memberData.pickle"  

class Data:
    def __init__(self, warnings, softbanned):
      self.warnings = warnings
      self.softbanned = softbanned

def load_data():
    if os.path.isfile(data_filename):
      with open(data_filename, "rb") as file:
        return pickle.load(file)
    else:
      return dict()

def load_member_data(member_ID):
  data = load_data()

  if member_ID not in data:
    return Data(0, False)

  return data[member_ID]

def save_member_data(member_ID, member_data):
  data = load_data()

  data[member_ID] = member_data

  with open(data_filename, "wb") as file:
    pickle.dump(data, file)





# --------------------------------------------------------------------------------------- #
# ----------------------------------- CLIENT COMMANDS ----------------------------------- #
# --------------------------------------------------------------------------------------- #




@client.command(pass_contect = True, name = 'ping', aliases=returnPossibleCaps('ping'))
async def ping(ctx):
  await ctx.send(f'Pong! **{round(client.latency * 1000)}ms**')
  
@client.command(pass_context = True, name = 'setuprules', aliases=returnPossibleCaps('setuprules'))
async def setuprules(ctx):
  global serverRules

  embed = discord.Embed(
    title="# 📜 SERVER RULES 📜",
    description=serverRules,
    colour = Color.pink()
  )
  
  if (ctx.author.id == 883536942711599127 or ctx.author.id == 743877445723095071):
    await ctx.send(embed=embed)

@client.command(pass_context = True, name = 'sendstring', aliases=returnPossibleCaps('sendstring'))
async def sendstring(ctx, *, string):
  if (ctx.author.id == 883536942711599127 or ctx.author.id == 743877445723095071):
    await ctx.send(string)

@client.command(pass_contect = True, name = 'warnings', aliases=returnPossibleCaps('warnings'))
async def warnings(ctx, member:Member = None):
  if (member == None):
    member = ctx.author
  
  userData = load_member_data(member.id)
  
  if (userData.warnings == 1):
    await ctx.send(f"**{member.display_name}** has {userData.warnings} warning.")
  else:
    await ctx.send(f"**{member.display_name}** has {userData.warnings} warnings.")

@client.command(pass_context = True, name = 'unwarn', aliases=returnPossibleCaps('unwarn'))
@commands.has_role("Trusted Staff Member")
async def unwarn(ctx, member:Member = None):
  if (member == ctx.author):
    await ctx.send(f'{ctx.author.mention} You cannot revoke warnings from yourself!')
    return
    
  userData = load_member_data(member.id)

  if (userData.warnings == 0):
    await ctx.send(f'Unable to unwarn **{member.display_name}** due to having zero warnings!')
    return

  userData.warnings = userData.warnings - 1

  embed = discord.Embed(
    title=f"{member.display_name} Has had a warning revoked!",
    description=f'**{member.display_name}** Has had a warning revoked by **{ctx.author.display_name}**',
    colour = Color.teal(),
    timestamp = datetime.utcnow()
  )

  embed.set_thumbnail(url=member.display_avatar.url)

  save_member_data(member.id, userData)
  
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')
  
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has had a warning revoked.")

@client.command(pass_context = True, name = 'warn', aliases=returnPossibleCaps('warn'))
@commands.has_role("Trusted Staff Member")
async def warn(ctx, member:Member = None, *, reason=None):
  if (member == ctx.author):
    await ctx.send(f'{ctx.author.mention} You cannot warn yourself!')
    return
    
  if (reason == None):
    await ctx.send(f'{ctx.author.mention} Please provide a valid reason!')
    return  
    
  userData = load_member_data(member.id)

  userData.warnings = userData.warnings + 1

  embed = discord.Embed(
    title=f"{member.display_name} Has been warned!",
    description=f"Reason: **{reason}**\nIssued By: **{ctx.author.display_name}**",
    colour = Color.red(),
    timestamp = datetime.utcnow()
  )

  save_member_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')
  
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has been warned.")

@client.command(pass_context = True, name = 'softban', aliases=returnPossibleCaps('softban'))
@commands.has_role("Trusted Staff Member")
async def softban(ctx, member:Member = None, *, reason=None):
  if (member == ctx.author):
    await ctx.send(f'{ctx.author.mention} You cannot soft-ban yourself!')
    return
    
  if (reason == None):
    await ctx.send(f'{ctx.author.mention} Please provide a valid reason!')
    return 
    
  userData = load_member_data(member.id)
  role = discord.utils.get(member.guild.roles, id=1120961059990290522)

  userData.softbanned = True

  embed = discord.Embed(
    title=f"{member.display_name} Has been soft-banned!",
    description=f"Reason: **{reason}**\nIssued By: **{ctx.author.display_name}**",
    colour = Color.red(),
    timestamp = datetime.utcnow()
  )

  save_member_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')

  await member.add_roles(role)
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has been soft-banned.")

@client.command(pass_context = True, name = 'revokeban', aliases=returnPossibleCaps('revokeban'))
@commands.has_role("Trusted Staff Member")
async def revokeban(ctx, member:Member = None):
  if (member == ctx.author):
    await ctx.send(f'{ctx.author.mention} You cannot unsoft-ban yourself!')
    return

  userData = load_member_data(member.id)
  role = discord.utils.get(member.guild.roles, id=1120961059990290522)

  userData.softbanned = False

  embed = discord.Embed(
    title=f"{member.display_name} Has had their soft-ban revoked!",
    description=f"**{member.display_name}** has had their soft-ban revoked by **{ctx.author.display_name}**",
    colour = Color.teal(),
    timestamp = datetime.utcnow()
  )

  save_member_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')

  await member.remove_roles(role)
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has had their soft-ban revoked.")

@client.command(pass_context = True, name = 'rules', aliases=returnPossibleCaps('rules'))
async def rules(ctx):
  global serverRules
  
  channel = await ctx.author.create_dm()
  
  await channel.send(serverRules)
  await ctx.send(f"{ctx.author.mention}, I have sent you the server rules in your DM's.")

@client.command(pass_context = True, name = 'report', aliases=returnPossibleCaps('report'))
async def report(ctx, member: Member=None, *, reason):
    if member == None:
      await ctx.send(f"{ctx.author.mention}, Please provid a valid member who you wish to report.")
      return;

    userData = load_member_data(member.id)

    embed = discord.Embed(
      title=f"{ctx.author.display_name} Has reported {member.display_name}!",
      description=f"Reason: **{reason}**",
      colour = Color.red(),
      timestamp = datetime.utcnow()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.set_footer(text=f'{userData.warnings} Warnings')
  
    await client.get_channel(1119789664287608912).send(embed=embed)
    await ctx.send(f"{ctx.author.mention}, Your report has went through. The staff will review your report!")




# -------------------------------------------------------------------------------------- #
# ----------------------------------- CLIENT HANDLER ----------------------------------- #
# -------------------------------------------------------------------------------------- #




keep_alive()
Token = os.environ['token']
client.run(Token)