# Apex Sigma: The Database Giant Discord Bot.
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

import secrets

import discord

from sigma.core.mechanics.command import SigmaCommand


async def send_log_message(cmd, message, reaction_url, reaction_id, reaction_name, inter_count):
        log_ch_id = cmd.cfg.get('log_ch')
        log_ch = discord.utils.find(lambda x: x.id == log_ch_id, cmd.bot.get_all_channels())
        if log_ch:
            author = f'{message.author.name}#{message.author.discriminator}'
            data_desc = f'Author: {author}'
            data_desc += f'\nAuthor ID: {message.author.id}'
            data_desc += f'\nGuild: {message.guild.name}'
            data_desc += f'\nGuild ID: {message.guild.id}'
            data_desc += f'\nReaction URL: [Here]({reaction_url})'
            data_desc += f'\nReaction ID: {reaction_id}'
            log_resp_title = f'🆙 Added {reaction_name.lower()} number {inter_count}'
            log_resp = discord.Embed(color=0x3B88C3)
            log_resp.add_field(name=log_resp_title, value=data_desc)
            log_resp.set_thumbnail(url=reaction_url)
            log_msg = await log_ch.send(embed=log_resp)
            return log_msg


def make_reaction_data(message, reaction_name, reaction_url, reaction_id, log_msg):
    return {
        'name': reaction_name.lower(),
        'user_id': message.author.id,
        'server_id': message.guild.id,
        'url': reaction_url,
        'reaction_id': reaction_id,
        'message_id': log_msg.id if log_msg else None
    }


async def addinteraction(cmd: SigmaCommand, message: discord.Message, args: list):
    if args:
        if len(args) >= 2:
            reaction_name = args[0]
            allowed_reactions = []
            for command in cmd.bot.modules.commands:
                if cmd.bot.modules.commands[command].category.lower() == 'interactions':
                    if command.name not in ['addinteraction', 'lovecalculator']:
                        allowed_reactions.append(command)
            if reaction_name.lower() in allowed_reactions:

            else:
                response = discord.Embed(color=0xBE1931, title=f'❗ No such interaction was found.')
        else:
            response = discord.Embed(color=0xBE1931, title=f'❗ Not enough arguments.')
    else:
        response = discord.Embed(color=0xBE1931, title=f'❗ Nothing inputted.')
    await message.channel.send(embed=response)
