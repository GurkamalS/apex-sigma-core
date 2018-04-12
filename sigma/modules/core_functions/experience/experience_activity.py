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

import secrets

from sigma.modules.core_functions.experience.experience_clock import add_exp


async def experience_activity(ev, message):
    if message.guild:
        if not await ev.bot.cool_down.on_cooldown(ev.name, message.author):
            if len(message.guild.members) >= 100:
                award_xp = 180
            else:
                award_xp = 150
            award_xp += secrets.randbelow(5) * 18
            add_exp(message.author, message.guild, award_xp)
            await ev.bot.cool_down.set_cooldown(ev.name, message.author, 80)
