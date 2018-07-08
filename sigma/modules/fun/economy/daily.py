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

import arrow
import discord

from sigma.core.mechanics.command import SigmaCommand


async def daily(cmd: SigmaCommand, message: discord.Message, args: list):
    daily_doc = await cmd.db[cmd.db.db_nam].DailyCache.find_one({'UserID': message.author.id}) or {}
    if not daily_doc:
        def_data = {'UserID': message.author.id, 'Stamp': 0, 'Streak': 0}
        await cmd.db[cmd.db.db_nam].DailyCache.insert_one(def_data)
    now_stamp = arrow.utcnow().timestamp
    last_daily = daily_doc.get('Stamp') or 0
    streak = daily_doc.get('Streak') or 0
    streak = 0 if now_stamp > last_daily + 172800 else streak
    streak += 1 if streak < 10 else 0
    if now_stamp > last_daily + 79200:
        currency = cmd.bot.cfg.pref.currency
        random_part = secrets.randbelow(100)
        amount = int(500 + random_part + (100 * (streak * 1.6))) if streak != 1 else 500 + random_part
        daily_data = {'UserID': message.author.id, 'Stamp': now_stamp, 'Streak': streak}
        await cmd.db.add_currency(message.author, message.guild, amount, additive=True)
        await cmd.db[cmd.db.db_nam].DailyCache.update_one({'UserID': message.author.id}, {'$set': daily_data})
        response = discord.Embed(color=0x66CC66, title=f'🎉 You got {amount} {currency} for a {streak}/10 streak.')
    else:
        next_stamp = last_daily + 79200
        response = discord.Embed(color=0x696969, title=f'🕙 Next daily available {arrow.get(next_stamp).humanize()}.')
    await message.channel.send(embed=response)
