import discord

from datetime import datetime

from Source.data_handler import save_data
from Source.data_handler import load_data

from discord import Color

client = None

soft_ban_role_id = 1120961059990290522

def set_client(new_client):
  global client
  
  client = new_client

async def warn_user(ctx, member, reason):
  userData = load_data(member.id)

  userData.warnings = userData.warnings + 1

  embed = discord.Embed(
    title=f"{member.display_name} Has been warned!",
    description=f"Reason: **{reason}**\nIssued By: **{ctx.author.display_name}**",
    colour = Color.red(),
    timestamp = datetime.utcnow()
  )

  save_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')
  
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has been warned.")

async def unwarn_user(ctx, member):
  userData = load_data(member.id)

  userData.warnings = userData.warnings - 1

  embed = discord.Embed(
    title=f"{member.display_name} Has had a warning revoked!",
    description=f'**{member.display_name}** Has had a warning revoked by **{ctx.author.display_name}**',
    colour = Color.teal(),
    timestamp = datetime.utcnow()
  )

  embed.set_thumbnail(url=member.display_avatar.url)

  save_data(member.id, userData)
  
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')
  
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has had a warning revoked.")

async def check_user_warnings(ctx, member):
  userData = load_data(member.id)
  
  if (userData.warnings == 1):
    await ctx.send(f"**{member.display_name}** has {userData.warnings} warning.")
  else:
    await ctx.send(f"**{member.display_name}** has {userData.warnings} warnings.")

async def soft_ban_user(ctx, member, reason):
  global soft_ban_role_id
  
  userData = load_data(member.id)
  role = discord.utils.get(member.guild.roles, id = soft_ban_role_id)

  userData.softbanned = True

  embed = discord.Embed(
    title=f"{member.display_name} Has been soft-banned!",
    description=f"Reason: **{reason}**\nIssued By: **{ctx.author.display_name}**",
    colour = Color.red(),
    timestamp = datetime.utcnow()
  )

  save_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')

  await member.add_roles(role)
  await client.get_channel(1118372347347476480).send(embed=embed)
  await ctx.send(f"{member.mention} Has been soft-banned.")

async def revoke_user_softban(ctx, member):
  global soft_ban_role_id
  
  userData = load_data(member.id)
  role = discord.utils.get(member.guild.roles, id = soft_ban_role_id)

  userData.softbanned = False

  embed = discord.Embed(
    title=f"{member.display_name} Has had their soft-ban revoked!",
    description=f"**{member.display_name}** has had their soft-ban revoked by **{ctx.author.display_name}**",
    colour = Color.teal(),
    timestamp = datetime.utcnow()
  )

  save_data(member.id, userData)

  embed.set_thumbnail(url=member.display_avatar.url)
  
  if (userData.warnings == 1):
    embed.set_footer(text=f'{userData.warnings} Warning')
  else:
    embed.set_footer(text=f'{userData.warnings} Warnings')

  await member.remove_roles(role)
  await client.get_channel(1118372347347476480).send(embed = embed)
  await ctx.send(f"{member.mention} Has had their soft-ban revoked.")

async def report_user(ctx, member, reason):
    userData = load_data(member.id)

    embed = discord.Embed(
      title=f"{ctx.author.display_name} Has reported {member.display_name}!",
      description=f"Reason: **{reason}**",
      colour = Color.red(),
      timestamp = datetime.utcnow()
    )

    embed.set_thumbnail(url=member.display_avatar.url)
  
    if (userData.warnings == 1):
      embed.set_footer(text=f'{userData.warnings} Warning')
    else:
      embed.set_footer(text=f'{userData.warnings} Warnings')
  
    await client.get_channel(1119789664287608912).send(embed = embed)
    await ctx.send(f"{ctx.author.mention}, Your report has went through. The staff will review your report!")