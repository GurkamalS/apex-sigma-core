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
import arrow
import discord
from humanfriendly.tables import format_pretty_table as boop

from sigma.core.mechanics.command import SigmaCommand


async def spouses(cmd: SigmaCommand, message: discord.Message, args: list):
    if message.mentions:
        target = message.mentions[0]
    else:
        target = message.author
    if args:
        page = args[0]
        try:
            page = int(page)
        except ValueError:
            page = 1
    else:
        page = 1
    if page < 1:
        page = 1
    start_range = 5 * (page - 1)
    end_range = 5 * page
    profile = await cmd.db[cmd.db.db_cfg.database].Profiles.find_one({'UserID': target.id}) or {}
    splist = profile.get('Spouses') or []
    spcount = len(splist)
    splist = splist[start_range:end_range]
    starter = 'You are' if target.id == message.author.id else f'{target.name} is'
    mid = 'have' if target.id == message.author.id else 'has'
    if splist:
        spdata = []
        for sp in splist:
            spmemb = discord.utils.find(lambda m: m.id == sp.get('UserID'), cmd.bot.get_all_members())
            spmemb = spmemb.name if spmemb else 'Unknown'
            sp_profile = await cmd.db[cmd.db.db_cfg.database].Profiles.find_one({'UserID': sp.get('UserID')}) or {}
            sp_spouses = sp_profile.get('Spouses') or []
            sp_spouse_ids = [s.get('UserID') for s in sp_spouses]
            sp_status = 'Married' if target.id in sp_spouse_ids else 'Proposed'
            spdata.append([spmemb, sp_status, arrow.get(sp.get('Time')).humanize().title()])
        spbody = boop(spdata, ['Name', 'Status', 'Since'])
        upgrades = await cmd.db[cmd.db.db_cfg.database].Upgrades.find_one({'UserID': target.id}) or {}
        limit = 10 + (upgrades.get('harem') or 0)
        response = discord.Embed(color=0xf9f9f9, title=f'💍 {starter} married to...')
        response.description = f'```hs\n{spbody}\n```'
        response.set_footer(text=f'[Page {page}] {target.name}\'s harem has {spcount}/{limit} people in it.')
    else:
        if page == 1:
            response = discord.Embed(color=0xe75a70, title=f'💔 {starter} not married, nor {mid} proposed, to anyone.')
        else:
            response = discord.Embed(color=0xe75a70, title=f'💔 {starter} has nobody on page {page}.')
    await message.channel.send(embed=response)
