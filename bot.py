import discord
import time
import asyncio


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


messages = joined = 0

token = read_token()
client = discord.Client()


async def update_status():
    await client.wait_until_ready()
    global messages, joined

    while not client.is_closed():
        try:
            with open("stat.csv", "a") as f:
                f.write(f"{int(time.time())}, {messages}, {joined}\n")

            messages = joined = 0

            await asyncio.sleep(300)
        except Exception as e:
            print(e)
            await asyncio.sleep(60)


@client.event
async def on_message(message):
    global messages
    messages += 1
    server_id = client.get_guild(611760401348165632)
    channels = ["not-spoken-shit-here"]

    if str(message.channel) in channels:
        if message.content == "!hello":
            await message.channel.send("Sup dawg!")
        elif message.content == "!users":
            await message.channel.send(f"Number of Members: {server_id.member_count}")
        elif message.content.startswith("!"):
            await message.channel.send(f"Wrong command retard {message.author.mention}, check !help.")


    if message.content == "!help":
        embed = discord.Embed(title="Read you illiterate fucks!", description="Commands")
        embed.add_field(name="!hello", value="Duh, greetings")
        embed.add_field(name="!users", value="Show amount of retards here.")
        await message.channel.send(embed=embed)


@client.event
async def on_join(member):
    global joined
    joined += 1
    for channel in member.server.channels:
        if str(channel) == "not-spoken-shit-here":
            await client.send_message(f"Welcome to the jungle retard {member.mention}!")


client.loop.create_task(update_status())
client.run(token)
