# -*- coding: utf-8 -*-

import discord
import asyncio

client = discord.Client()

async with client.login('Ift3na0Hx4xYzS7co3EH68phmz3FZriV') as client:
    await client.login()
    channel = client.get_server('184487341430276097')
    print("---")
    print(channel)


