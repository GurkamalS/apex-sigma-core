# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2017  Lucia's Cipher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import aiohttp
import discord
import json

from sigma.core.mechanics.command import SigmaCommand


async def dog(cmd: SigmaCommand, message: discord.Message, args: list):
    doggie_url = 'https://api.thedogapi.co.uk/v2/dog.php'
    async with aiohttp.ClientSession() as session:
        async with session.get(doggie_url) as data:
            doggie_data = await data.read()
    image_url = json.loads(doggie_data).get('data')[0].get('url')
    response = discord.Embed(color=0xf9f9f9, title='🐶 Woof!')
    response.set_image(url=image_url)
    await message.channel.send(embed=response)
