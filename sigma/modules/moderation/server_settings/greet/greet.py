﻿# Apex Sigma: The Database Giant Discord Bot.
# Copyright (C) 2018  Lucia's Cipher
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

import discord

from sigma.core.mechanics.command import SigmaCommand
from sigma.core.utilities.generic_responses import permission_denied


async def greet(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.author.permissions_in(message.channel).manage_guild:
        active = await cmd.db.get_guild_settings(message.guild.id, 'greet')
        active = True if active is None else active
        if active:
            state, ender = False, 'disabled'
        else:
            state, ender = True, 'enabled'
        await cmd.db.set_guild_settings(message.guild.id, 'greet', state)
        response = discord.Embed(color=0x77B255, title=f'✅ Greeting Messages {ender}.')
    else:
        response = permission_denied('Manage Server')
    await message.channel.send(embed=response)
