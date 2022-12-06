import discord
from discord.ext import commands
import os
from functions import add_suscription, remove_suscription, list_suscriptions, valid_rss, parse_and_upload_to_db
from dotenv import load_dotenv


load_dotenv()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("pong")

@bot.command()
async def add(ctx, rss: str):
    if valid_rss(rss):
        res = add_suscription(rss)
        parse_and_upload_to_db([rss], False)
        await ctx.send(res)
    else:
        await ctx.send("la url no es valida")

@bot.command()
async def remove(ctx, index: int):
    res = remove_suscription(index)
    await ctx.send(res)

@bot.command()
async def list(ctx):
    suscriptions = list_suscriptions()
    msg = ""
    for i, rss in enumerate(suscriptions):
        msg = msg + f"[{i}] {rss}\n"
    await ctx.send(f"Estas son tus suscripciones:\n{msg}")

bot.run(os.environ.get("bot_token"))