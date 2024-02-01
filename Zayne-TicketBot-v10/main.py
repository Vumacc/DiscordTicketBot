import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents) # Replace ! with whatever prefix you want for bot commands

SupportRole = "Support"  # Replace with the actual name of the role you want the support role to be

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def createticket(ctx):
    if ctx.channel.id != CHANNEL: # Replace CHANNEL with the create a ticket's channel ID
        return
    guild = ctx.guild
    
    # Make sure to change the name "Tickets" to the category where you want the ticket channels to be made.    
    category = discord.utils.get(guild.categories, name="tickets") 
    ticket_channel = await guild.create_text_channel(name=f'ticket-{ctx.author.name}', category=category)

    # Change the welcome_message to whatever you would like
    welcome_message = f"Welcome to your ticket, {ctx.author.mention}!"
    await ticket_channel.send(welcome_message)


# Command to Close tickets if the user closing it has the support role (go to line #9 to rename your support role to the role you want to use)
@bot.command()
@commands.has_role(SupportRole)
async def closeticket(ctx, *, reason: str):
    if ctx.channel.category.name == "tickets" and ctx.channel.name.startswith("ticket-"):
        user = ctx.channel.name.replace("ticket-", "")
        member = discord.utils.get(ctx.guild.members, name=user)
        if member:
            status_message = f"Your ticket has been closed. Reason: {reason}"
            await member.send(status_message)
        await ctx.channel.delete()
        await ctx.send(f"Ticket closed! Reason: {reason}")
    else:
        await ctx.send("This command can only be used in a ticket channel.")

# Command to add users to tickets via either User ID or mention if the user adding someone has the support role (go to line #9 to rename your support role to the role you want to use)
@bot.command()
@commands.has_role(SupportRole)
async def adduser(ctx, user: discord.User):
    if ctx.channel.category.name == "tickets" and ctx.channel.name.startswith("ticket-"):
        await ctx.channel.set_permissions(user, read_messages=True, send_messages=True)
        await ctx.send(f"{user.mention} has been added to the ticket.")
    else:
        await ctx.send("This command can only be used in a ticket channel.")



bot.run("TOKEN") # Replace TOKEN with your bot token
