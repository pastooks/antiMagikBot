# This example requires the 'message_content' intent.
import json

import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def writeMap(fileName: str):
    f = open(fileName)
    tempMap = json.load(f)
    retMap = {}
    for i in tempMap.keys():
        retMap[int(i)] = tempMap[i]
    return retMap

checkMap = writeMap('mapStore.json')  # if json lost replace with {}
embedList = ["link", "article", "video"]
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print(checkMap)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for <help"))

@client.event
async def on_message(message):

    users = checkMap.keys()

    if message.author == client.user:
        return

    if message.author.id == 439205512425504771:  # notsobot
        if message.reference is not None:  # is a reply
            repliedToID = message.reference.message_id
            repliedTo = await message.channel.fetch_message(repliedToID)
            if repliedTo.reference is not None:  # is a reply to the origin image
                originID = repliedTo.reference.message_id
                origin = await message.channel.fetch_message(originID)
                if origin.author.id in users:  # if source is on list
                    if origin.author.id != repliedTo.author.id:  # if source is not requester
                        for string in checkMap[origin.author.id]:
                            if string == "all":  # if universal blacklist
                                await message.delete()
                                await repliedTo.reply(':thumbsdown:')
                                return
                            if string in repliedTo.content:  # if blacklist includes used command
                                await message.delete()
                                await repliedTo.reply(':thumbsdown:')
                                return
            else:  # look for origin image
                async for checkMe in message.channel.history(limit=100):  # for every message in the past 100 messages
                    if checkMe.id != message.id:  # skip inciting message
                        if len(checkMe.attachments) != 0:  # message has attachments
                            for i in checkMe.attachments:
                                if i.content_type.startswith("image"):  # message has an image
                                    if checkMe.author.id in users:  # is from a blocked user
                                        for string in checkMap[checkMe.author.id]:
                                            if string == "all":  # if universal blacklist
                                                await message.delete()
                                                await repliedTo.reply(':thumbsdown:')
                                                return
                                            if string in repliedTo.content:  # if blacklist includes used command
                                                await message.delete()
                                                await repliedTo.reply(':thumbsdown:')
                                                return
                                    return  # source is safe
                        if len(checkMe.embeds) != 0:  # message has embeds
                            for i in checkMe.embeds:
                                if i.type not in embedList:  # embed is 100% an image (rich moment, might get false positives)
                                    if checkMe.author.id in users:  # is from a blocked user
                                        for string in checkMap[checkMe.author.id]:
                                            if string == "all":  # if universal blacklist
                                                await message.delete()
                                                await repliedTo.reply(':thumbsdown:')
                                                return
                                            if string in repliedTo.content:  # if blacklist includes used command
                                                await message.delete()
                                                await repliedTo.reply(':thumbsdown:')
                                                return
                                    return  # source(?) is safe
        return

    # bot commands
    if message.content == "<help":
        await message.reply("i hate you notsobot\n\nuse `<addme` to block notsobot commands\nuse `<removeme` to unblock notsobot commands\n\nwhen on list use `<blacklist` and `<unblacklist` to block/unblock specific notso commands\nif no blacklist is made all notsobot commands are blocked\nformat is `<blacklist [command]`, with `[command]` being replacable by any command (without prefix)\ncheck current blacklist with `<checklist`")
        return

    if message.content == "<addme":
        if message.author.id in users:
            await message.reply('already in')
        else:
            checkMap[message.author.id] = ["all"]
            await message.reply('done, to customize blacklist use `<blacklist [command]`')

        json_object = json.dumps(checkMap, indent=4)
        with open("mapStore.json", "w") as outfile:
            outfile.write(json_object)
        return

    if message.content == "<removeme":
        if message.author.id in users:
            del checkMap[message.author.id]
            await message.reply('done')
        else:
            await message.reply('not in list')

        json_object = json.dumps(checkMap, indent=4)
        with open("mapStore.json", "w") as outfile:
            outfile.write(json_object)
        return

    if message.content.startswith("<blacklist"):
        parsed = message.content.split()
        if len(parsed) != 2:
            await message.reply("invalid number of arguments (only one word following command)")
            return
        elif parsed[1] == "all":
            if checkMap[message.author.id] == ["all"]:
                await message.reply("user already has universal blacklist")
            else:
                checkMap[message.author.id] = ["all"]
                await message.reply("done, universal blacklist set")
            return
        if message.author.id in users:
            if checkMap[message.author.id] == ["all"]:
                checkMap[message.author.id] = [parsed[1]]
                await message.reply("done, universal blacklist no longer applies")
            else:
                tempList = checkMap[message.author.id]
                if parsed[1] in tempList:
                    await message.reply("already blacklisted")
                else:
                    tempList.append(parsed[1])
                    checkMap[message.author.id] = tempList
                    await message.reply("done")

            json_object = json.dumps(checkMap, indent=4)
            with open("mapStore.json", "w") as outfile:
                outfile.write(json_object)
        else:
            await message.reply("user does not have blacklist, to begin one use `<addme`")
        return

    if message.content.startswith("<unblacklist"):
        parsed = message.content.split()
        if len(parsed) != 2:
            await message.reply("invalid number of arguments (only one word following command)")
            return
        elif parsed[1] == "all":
            await message.reply("haha funny")
            return
        if message.author.id in users:
            if checkMap[message.author.id] == ["all"]:
                checkMap[message.author.id] = [parsed[1]]
            else:
                tempList = checkMap[message.author.id]
                if parsed[1] in tempList:
                    tempList.remove(parsed[1])
                    if len(tempList) == 0:
                        await message.reply("all blacklisted commands removed, universal blacklist applied. to instead have no blacklist, use `<removeme`")
                        checkMap[message.author.id] = ["all"]
                    else:
                        checkMap[message.author.id] = tempList
                        await message.reply("done")
                else:
                    await message.reply("command not in blacklist")

            json_object = json.dumps(checkMap, indent=4)
            with open("mapStore.json", "w") as outfile:
                outfile.write(json_object)
        else:
            await message.reply("user does not have blacklist, to begin one use `<addme`")
        return

    if message.content == "<checklist":
        if message.author.id in users:
            if checkMap[message.author.id] == ["all"]:
                await message.reply("universal blacklist")
            else:
                await message.reply(checkMap[message.author.id])
        else:
            await message.reply("user does not have blacklist, to begin one use `<addme`")
        return

    return



client.run('')