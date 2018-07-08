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
from sigma.core.utilities.data_processing import user_avatar
from sigma.modules.minigames.professions.nodes.item_core import get_item_core


async def inspect(cmd: SigmaCommand, message: discord.Message, args: list):
    item_core = await get_item_core(cmd.db)
    if args:
        inv = await cmd.db.get_inventory(message.author)
        if inv:
            lookup = ' '.join(args)
            item_o = item_core.get_item_by_name(lookup)
            if item_o:
                item = await cmd.db.get_inventory_item(message.author, item_o.file_id)
            else:
                item = None
            if item:
                response = item_o.make_inspect_embed(cmd.bot.cfg.pref.currency)
                stat_coll = cmd.db[cmd.db.db_nam].ItemStatistics
                all_stats = await stat_coll.find_one({'UserID': message.author.id}) or {}
                item_total = 0
                all_stat_docs = await stat_coll.find({item_o.file_id: {'$exists': True}}).to_list(None)
                for stat_doc in all_stat_docs:
                    item_total += stat_doc.get(item_o.file_id) or 0
                stat_count = all_stats.get(item_o.file_id) or 0
                footer = f'You Found: {stat_count} | Total Found: {item_total} | ItemID: {item["item_id"]}'
                response.set_footer(text=footer)
            else:
                response = None
        else:
            response = None
    else:
        response = discord.Embed(color=0xBE1931, title='❗ Nothing inputted.')
    if not response:
        lookup = ' '.join(args)
        item = item_core.get_item_by_name(lookup)
        if item:
            if item.rarity != 0:
                stat_coll = cmd.db[cmd.db.db_nam].ItemStatistics
                all_stats = await stat_coll.find_one({'UserID': message.author.id}) or {}
                item_total = 0
                all_stat_docs = await stat_coll.find({item.file_id: {'$exists': True}}).to_list(None)
                for stat_doc in all_stat_docs:
                    item_total += stat_doc.get(item.file_id) or 0
                stat_count = all_stats.get(item.file_id) or 0
                response = item.make_inspect_embed(cmd.bot.cfg.pref.currency)
                response.set_footer(text=f'You Found: {stat_count} | Total Found: {item_total}')
            else:
                response = discord.Embed(color=0xBE1931, title='❗ Sorry but that\'s trash.')
        else:
            response = discord.Embed(color=0x696969, title=f'🔍 Item not found.')
    else:
        response.set_author(name=message.author.display_name, icon_url=user_avatar(message.author))
    await message.channel.send(embed=response)
