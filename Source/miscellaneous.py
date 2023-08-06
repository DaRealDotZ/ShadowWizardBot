from Source.utility import send_embed_in_dm

async def send_rules_in_dm(ctx, rules):
  await send_embed_in_dm(ctx, "📜 SERVER RULES 📜", rules)
  await ctx.send(f"{ctx.author.mention}, I have sent you the server rules in your DM's.")