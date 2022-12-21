# This example requires the 'message_content' intent.

import discord
import csv

intents = discord.Intents.default()
intents.message_content = True

def writeList(fileName: str):
    retList = []
    fileOpened = open(fileName, newline='\n')
    fileReader = csv.reader(fileOpened)
    tempList = []
    for row in fileReader:
        tempList = row
    for i in tempList:
        retList.append(int(i))
    print(retList)
    return retList

client = discord.Client(intents=intents)
checkList = writeList('listStore.csv')
embedList = ["link", "article", "video"]
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == 439205512425504771:  # notsobot
        if message.reference is not None:  # is a reply
            repliedToID = message.reference.message_id
            repliedTo = await message.channel.fetch_message(repliedToID)
            if repliedTo.reference is not None:  # is a reply to the origin image
                originID = repliedTo.reference.message_id
                origin = await message.channel.fetch_message(originID)
                if checkList.__contains__(origin.author.id):
                    if origin.author.id != repliedTo.author.id:
                        await message.delete()
                        await repliedTo.reply(':thumbsdown:')
            else:  # look for origin image
                # uhhh
                #print(message.id)
                async for checkMe in message.channel.history(limit=100):  # for every message in the past 100 messages
                    #print(checkMe.author)
                    #print(checkMe.id)
                    if checkMe.id != message.id:  # skip inciting message
                        #print(checkMe.attachments)
                        #print(checkMe.embeds)
                        #print(checkMe.content)
                        if len(checkMe.attachments) != 0:  # message has attachments
                            for i in checkMe.attachments:
                                if i.content_type.startswith("image"):  # message has an image
                                    if checkList.__contains__(checkMe.author.id):
                                        if checkMe.author.id != repliedTo.author.id:
                                            await message.delete()
                                            await repliedTo.reply(':thumbsdown:')
                                    return
                        if len(checkMe.embeds) != 0:  # message has embeds
                            for i in checkMe.embeds:
                                #print(i.type)
                                if not embedList.__contains__(i.type):
                                    if checkList.__contains__(checkMe.author.id):
                                        if checkMe.author.id != repliedTo.author.id:
                                            await message.delete()
                                            await repliedTo.reply(':thumbsdown:')
                            return
        return

    # else
    if message.content == "<addme":
        if checkList.__contains__(message.author.id):
            await message.reply('already in')
        else:
            checkList.append(message.author.id)
            await message.reply('done')
        newFile = open('listStore.csv', 'w', newline='\n')
        newWrite = csv.writer(newFile)
        newWrite.writerow(checkList)
        return

    if message.content == "<removeme":
        if checkList.__contains__(message.author.id):
            checkList.remove(message.author.id)
            await message.reply('done')
        else:
            await message.reply('not in list')
        newFile = open('listStore.csv', 'w', newline='\n')
        newWrite = csv.writer(newFile)
        newWrite.writerow(checkList)
        return

client.run('')